#!/usr/bin/env python3
"""
PreciosCerca - Servidor Principal (Flask)
=========================================

Servidor Flask que proporciona una API REST para la app de lista de compras.
Soporta búsqueda de productos con filtro por supermercado.

Endpoints principales:
- GET /products?query=X&supermercado=Y - Buscar productos (filtro opcional)
- POST /lista - Agregar producto a lista
- GET /lista - Ver lista completa
- DELETE /lista/<id> - Eliminar de lista

Supermercados activos:
- Carrefour (API VTEX) ✅
- Día % (API REST) ✅
- La Reina (HTML Scraping) ✅

Autor: PreciosCerca Team
Fecha: Noviembre 2025
"""

from flask import Flask, jsonify, request
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from functools import lru_cache
from datetime import datetime, timedelta, time as datetime_time
import pytz

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 Inicializando PreciosCerca Server...")

try:
    from productos.scrapers.scraper_carrefour import ScraperCarrefour
    from productos.scrapers.scraper_dia import ScraperDia
    from productos.scrapers.scraper_lareina import ScraperLaReina
    from productos.scrapers.scraper_lagallega import ScraperLaGallega
    from productos.scrapers.scraper_coto import ScraperCoto
    from lista_compras import lista_compras_global
    from productos.services import buscar_productos_similares
    print("✅ Scrapers cargados: Carrefour, Día %, La Reina, La Gallega, Coto")
    print("✅ Sistema de lista de compras inicializado")
except Exception as e:
    print(f"❌ Error cargando scrapers: {e}")
    sys.exit(1)

app = Flask(__name__)

# Inicializar scrapers disponibles (TODOS OPTIMIZADOS + Coto)
scrapers = {
    'carrefour': ScraperCarrefour(),
    'dia': ScraperDia(),
    'lareina': ScraperLaReina(),      # ✅ OPTIMIZADO: Solo 9 categorías principales
    'lagallega': ScraperLaGallega(),  # ✅ OPTIMIZADO: Solo 20 categorías principales
    'coto': ScraperCoto()             # ✅ HTML Scraping - Coto Digital
}

# CACHÉ DE PRODUCTOS EN MEMORIA (se refresca automáticamente)
# Formato: {supermercado: {timestamp: datetime, productos: []}}
productos_cache = {}
CACHE_DURACION_MINUTOS = 30  # Caché válido por 30 minutos

print(f"✅ {len(scrapers)} scrapers activos con caché inteligente")

# ========== FUNCIÓN HELPER: HORARIO DE MANTENIMIENTO ==========
def es_horario_mantenimiento():
    """
    Verifica si el servidor está en horario de mantenimiento (precarga diaria).
    Horario: 7:30 AM - 8:30 AM (hora Argentina UTC-3)
    """
    try:
        # Zona horaria de Argentina
        tz_argentina = pytz.timezone('America/Argentina/Buenos_Aires')
        ahora = datetime.now(tz_argentina)
        hora_actual = ahora.time()
        
        # Ventana de mantenimiento: 7:30 - 8:30 AM
        mantenimiento_inicio = datetime_time(7, 30)
        mantenimiento_fin = datetime_time(8, 30)
        
        return mantenimiento_inicio <= hora_actual <= mantenimiento_fin
    except Exception as e:
        print(f"⚠️ Error verificando horario de mantenimiento: {e}")
        return False  # En caso de error, permitir acceso normal

# ========== ENDPOINT PRINCIPAL: BUSCAR PRODUCTOS ==========
@app.route('/products', methods=['GET'])
def buscar_productos():
    """
    Endpoint principal para buscar productos con filtro opcional por supermercado.
    
    Parámetros GET:
    - query (obligatorio): término de búsqueda (ej: "leche", "pan", "dulce de leche")
    - supermercado (opcional): filtrar por "carrefour", "dia" o "lareina"
    - page (opcional): número de página (default: 1)
    - limit (opcional): productos por página (default: 30, max: 100)
    
    Ejemplos:
    - /products?query=leche&supermercado=carrefour  (solo Carrefour, página 1, 30 productos)
    - /products?query=pan&page=2&limit=30           (todos, página 2, 30 productos)
    - /products?query=aceite&limit=50                (todos, página 1, 50 productos)
    
    Retorna JSON con productos ordenados por precio:
    {
        "query": "leche",
        "total_encontrados": 150,
        "page": 1,
        "limit": 30,
        "total_pages": 5,
        "has_more": true,
        "supermercados_consultados": ["Carrefour"],
        "productos_por_supermercado": {"Carrefour": 150},
        "resultados": [...]
    }
    """
    # ✅ VERIFICAR HORARIO DE MANTENIMIENTO (7:30-8:30 AM)
    if es_horario_mantenimiento():
        return jsonify({
            'maintenance': True,
            'message': 'El servidor está actualizando el catálogo de productos (8:00 AM). Por favor intenta de nuevo en unos minutos.',
            'retry_after': '8:30 AM',
            'status': 'maintenance'
        }), 503
    
    query = request.args.get('query', request.args.get('q', 'leche'))
    filtro_super = request.args.get('supermercado', '').lower()
    
    # Parámetros de paginación
    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 30)), 100)  # Max 100 por página
    except ValueError:
        page = 1
        limit = 30
    
    if filtro_super:
        print(f"🔍 Búsqueda: '{query}' en {filtro_super.upper()}")
    else:
        print(f"🔍 Búsqueda: '{query}' en todos los supermercados")
    
    try:
        inicio = time.time()
        todos_los_productos = []
        supermercados_consultados = []
        productos_por_supermercado = {}
        
        # Determinar qué scrapers usar
        scrapers_a_usar = {}
        if filtro_super:
            # Buscar solo en el supermercado especificado
            if filtro_super in scrapers:
                scrapers_a_usar[filtro_super] = scrapers[filtro_super]
            else:
                return jsonify({
                    'error': f'Supermercado "{filtro_super}" no disponible',
                    'supermercados_disponibles': list(scrapers.keys())
                }), 400
        else:
            # Buscar en todos
            scrapers_a_usar = scrapers
        
        # BÚSQUEDA EN PARALELO (SIN LÍMITES)
        def buscar_en_supermercado(nombre_super, scraper_obj):
            """Función auxiliar para buscar en un supermercado (ejecutar en thread)"""
            try:
                print(f"  🔍 Buscando en {nombre_super}...")
                productos = scraper_obj.buscar_productos(query)
                # Aplicar filtro para búsquedas de múltiples palabras
                productos = buscar_productos_similares(query, productos)
                print(f"  ✅ {nombre_super}: {len(productos)} productos")
                return nombre_super, productos
            except Exception as e:
                print(f"  ❌ {nombre_super}: Error - {e}")
                return nombre_super, []
        
        # Mapeo de nombres display
        NOMBRES_DISPLAY = {
            'carrefour': 'Carrefour',
            'dia': 'Día %',
            'lareina': 'La Reina',
            'lagallega': 'La Gallega'
        }
        
        # Ejecutar búsquedas en paralelo (máx 4 threads)
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Crear futures para cada scraper
            futures = {
                executor.submit(buscar_en_supermercado, NOMBRES_DISPLAY[key], scraper): key 
                for key, scraper in scrapers_a_usar.items()
            }
            
            # Recolectar resultados a medida que terminan
            for future in as_completed(futures):
                nombre_super, productos = future.result()
                if productos:
                    todos_los_productos.extend(productos)
                    supermercados_consultados.append(nombre_super)
                    productos_por_supermercado[nombre_super] = len(productos)
        
        # NO ordenar por precio aquí - services.py ya ordenó por relevancia+precio
        # Esto mantiene la priorización de productos con todas las palabras de búsqueda
        
        # Convertir al formato que espera la app Android
        resultados = []
        for producto in todos_los_productos:
            resultados.append({
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'supermercado': producto['supermercado'],
                'fecha': '2025-11-03',
                'relevancia': 1.0,
                'url': producto.get('url', ''),
                'imagen': producto.get('imagen', '')  # Agregar imagen
            })
        
        tiempo_total = time.time() - inicio
        print(f"✅ {len(resultados)} productos encontrados en {tiempo_total:.2f}s")
        
        # PAGINACIÓN: calcular offset y slice
        total_productos = len(resultados)
        total_pages = (total_productos + limit - 1) // limit  # Redondeo hacia arriba
        offset = (page - 1) * limit
        resultados_paginados = resultados[offset:offset + limit]
        
        print(f"📄 Página {page}/{total_pages} - Mostrando {len(resultados_paginados)} productos")
        
        # Respuesta en formato Android con paginación
        response = {
            'query': query,
            'total_encontrados': total_productos,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'has_more': page < total_pages,
            'supermercados_consultados': supermercados_consultados,
            'productos_por_supermercado': productos_por_supermercado,
            'resultados': resultados_paginados
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return jsonify({
            'error': str(e),
            'query': query,
            'total_encontrados': 0,
            'supermercados_consultados': [],
            'productos_por_supermercado': {},
            'resultados': []
        }), 500

@app.route('/products-cercanos', methods=['GET'])
def buscar_productos_cercanos():
    """Busca productos en supermercados con sucursales cercanas al usuario (GPS).
    
    NOTA: Este endpoint está en desarrollo. Actualmente solo funciona con La Gallega.
    Los scrapers de Carrefour, Día % y La Reina no tienen datos de sucursales implementados.
    
    Parámetros: query, lat, lng, radio (km)
    """
    query = request.args.get('query', 'leche')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radio = request.args.get('radio', default=50, type=float)
    
    if lat is None or lng is None:
        return jsonify({
            'error': 'Se requieren parámetros: query, lat, lng'
        }), 400
    
    print(f"🔍 Búsqueda cercana: '{query}' en ({lat}, {lng}) - Radio: {radio}km")
    
    try:
        # Detectar ciudad del usuario
        info_ciudad = detectar_ciudad_usuario(lat, lng)
        ciudad_usuario = info_ciudad['ciudad']
        distancia_ciudad = info_ciudad['distancia_km']
        
        print(f"  📍 Ciudad detectada: {ciudad_usuario} (a {distancia_ciudad}km del centro)")
        
        # Obtener supermercados con sucursales cercanas
        supermercados_cercanos = obtener_supermercados_cercanos(lat, lng, radio)
        
        if not supermercados_cercanos:
            print(f"  ⚠️ No hay supermercados dentro de {radio}km")
            return jsonify({
                'query': query,
                'lat': lat,
                'lng': lng,
                'radio_km': radio,
                'ciudad_detectada': ciudad_usuario,
                'distancia_ciudad_km': distancia_ciudad,
                'mensaje': f'No hay supermercados con sucursales dentro de {radio}km de tu ubicación en {ciudad_usuario}',
                'total_encontrados': 0,
                'supermercados_consultados': [],
                'productos_por_supermercado': {},
                'resultados': []
            })
        
        print(f"  📍 Supermercados con sucursales cercanas: {', '.join(supermercados_cercanos)}")
        
        # Obtener info detallada de sucursales cercanas y calcular distancia mínima por supermercado
        sucursales_info = filtrar_sucursales_por_radio(lat, lng, radio)
        distancias_supermercados = {}
        
        # Mostrar sucursales encontradas y guardar distancia mínima
        for super_nombre, sucursales_lista in sucursales_info.items():
            sucursal_mas_cercana = sucursales_lista[0]  # Ya están ordenadas por distancia
            distancias_supermercados[super_nombre] = sucursal_mas_cercana['distancia_km']
            print(f"    • {super_nombre}: {len(sucursales_lista)} sucursal(es), más cercana a {sucursal_mas_cercana['distancia_km']}km")
        
        # Ordenar supermercados por distancia (más cercano primero)
        supermercados_ordenados = sorted(
            supermercados_cercanos,
            key=lambda s: distancias_supermercados.get(s, float('inf'))
        )
        
        supermercado_mas_cercano = supermercados_ordenados[0] if supermercados_ordenados else None
        distancia_mas_cercano = distancias_supermercados.get(supermercado_mas_cercano, 0) if supermercado_mas_cercano else 0
        
        print(f"  🏆 Supermercado más cercano: {supermercado_mas_cercano} a {distancia_mas_cercano:.2f}km")
        
        # Buscar productos solo en supermercados cercanos
        todos_los_productos = []
        supermercados_consultados = []
        productos_por_supermercado = {}
        
        # Mapeo de nombres de supermercados a keys de scrapers
        MAPEO_SCRAPERS = {
            'La Gallega': 'lagallega'
            # 'Carrefour': 'carrefour',
            # 'Día %': 'dia',
            # 'La Reina': 'lareina'
        }
        
        # Buscar en supermercados en orden de cercanía
        for nombre_super in supermercados_ordenados:
            scraper_key = MAPEO_SCRAPERS.get(nombre_super)
            
            # Solo buscar si tenemos scraper funcional para ese supermercado
            if scraper_key and scraper_key in scrapers:
                scraper = scrapers[scraper_key]
                
                print(f"  🔍 Buscando en {nombre_super}...")
                try:
                    productos = scraper.buscar_productos(query)
                    if productos:
                        # Cambiar el nombre del supermercado en los resultados
                        # y agregar la distancia de la sucursal más cercana
                        for prod in productos:
                            prod['supermercado'] = nombre_super
                            prod['distancia_sucursal_km'] = distancias_supermercados.get(nombre_super, 0)
                        todos_los_productos.extend(productos)
                        supermercados_consultados.append(nombre_super)
                        productos_por_supermercado[nombre_super] = len(productos)
                        print(f"  ✅ {nombre_super}: {len(productos)} productos")
                    else:
                        print(f"  ℹ️ {nombre_super}: sin resultados para '{query}'")
                except Exception as e:
                    print(f"  ⚠️ {nombre_super}: error al buscar - {e}")
            else:
                print(f"  ⚠️ {nombre_super}: scraper no disponible (sucursales cercanas pero sin scraper funcional)")
        
        # Ordenar productos: primero por distancia del supermercado (más cercano primero), luego por precio
        todos_los_productos.sort(key=lambda x: (x.get('distancia_sucursal_km', float('inf')), x['precio']))
        
        # Formatear respuesta
        resultados = []
        for producto in todos_los_productos:
            resultados.append({
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'supermercado': producto['supermercado'],
                'distancia_sucursal_km': producto.get('distancia_sucursal_km', 0),
                'fecha': '2025-10-30',
                'relevancia': 1.0,
                'url': producto.get('url', '')
            })
        
        print(f"✅ {len(resultados)} productos encontrados en {len(supermercados_consultados)} supermercado(s) cerca de {ciudad_usuario}")
        
        response = {
            'query': query,
            'lat': lat,
            'lng': lng,
            'radio_km': radio,
            'ciudad_detectada': ciudad_usuario,
            'distancia_ciudad_km': distancia_ciudad,
            'supermercado_mas_cercano': supermercado_mas_cercano,
            'distancia_supermercado_mas_cercano_km': distancia_mas_cercano,
            'total_encontrados': len(resultados),
            'supermercados_consultados': supermercados_consultados,
            'productos_por_supermercado': productos_por_supermercado,
            'sucursales_cercanas': sucursales_info,
            'resultados': resultados
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error en búsqueda cercana: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'query': query,
            'total_encontrados': 0,
            'resultados': []
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor funciona."""
    return jsonify({
        'status': 'OK', 
        'message': 'PreciosCerca Server funcionando',
        'scrapers_disponibles': list(scrapers.keys()),
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def info():
    """Información básica del servidor."""
    return jsonify({
        'app': 'PreciosCerca API',
        'descripcion': 'API para comparar precios en supermercados argentinos',
        'supermercados_soportados': list(scrapers.keys()),
        'endpoints': {
            '/products?query=TERMINO': 'Buscar productos en todos los supermercados',
            '/products-cercanos?query=TERMINO&lat=LAT&lng=LNG&radio=KM': 'Buscar solo en supermercados cercanos (NEW)',
            '/sucursal-cercana?supermercado=NOMBRE&lat=LAT&lng=LNG': 'Encontrar sucursal más cercana',
            '/sucursales?supermercado=NOMBRE': 'Listar sucursales de un supermercado',
            '/health': 'Estado del servidor'
        }
    })

@app.route('/sucursal-cercana', methods=['GET'])
def sucursal_cercana():
    """Busca sucursal más cercana (EN DESARROLLO - solo La Gallega)"""
    return jsonify({
        'error': 'Función en desarrollo',
        'mensaje': 'Búsqueda de sucursales estará disponible próximamente'
    }), 501

@app.route('/sucursales', methods=['GET'])
def listar_sucursales():
    """Lista sucursales (EN DESARROLLO - solo La Gallega)"""
    return jsonify({
        'error': 'Función en desarrollo',
        'mensaje': 'Listado de sucursales estará disponible próximamente'
    }), 501


# ============================================================================
# ENDPOINTS DE LISTA DE COMPRAS
# ============================================================================

@app.route('/lista-compras', methods=['GET'])
def obtener_lista_compras():
    """Obtiene todos los items de la lista de compras"""
    try:
        items = lista_compras_global.obtener_items()
        return jsonify({
            'items': items,
            'total_items': lista_compras_global.cantidad_items()
        })
    except Exception as e:
        print(f"❌ Error obteniendo lista de compras: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lista-compras/agregar', methods=['POST'])
def agregar_a_lista():
    """
    Agrega un producto a la lista de compras
    Body JSON: {"nombre": "Leche", "cantidad": 1, "precio": 150.50, "supermercado": "Carrefour", "imagen": "url"}
    """
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        cantidad = data.get('cantidad', 1)
        precio = data.get('precio', 0.0)
        supermercado = data.get('supermercado', '')
        imagen = data.get('imagen', '')
        
        if not nombre:
            return jsonify({'error': 'Nombre de producto requerido'}), 400
        
        resultado = lista_compras_global.agregar_producto(
            nombre, cantidad, precio, supermercado, imagen
        )
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Error agregando a lista: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lista-compras/eliminar', methods=['DELETE'])
def eliminar_de_lista():
    """
    Elimina un producto de la lista de compras
    Body JSON: {"nombre": "Leche"}
    """
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        
        if not nombre:
            return jsonify({'error': 'Nombre de producto requerido'}), 400
        
        resultado = lista_compras_global.eliminar_producto(nombre)
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Error eliminando de lista: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lista-compras/limpiar', methods=['POST'])
def limpiar_lista():
    """Limpia todos los items de la lista de compras"""
    try:
        lista_compras_global.limpiar()
        return jsonify({
            'status': 'ok',
            'mensaje': 'Lista de compras limpiada'
        })
    except Exception as e:
        print(f"❌ Error limpiando lista: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lista-compras/comparar', methods=['GET'])
def comparar_lista():
    """Compara precios de la lista entre supermercados (EN DESARROLLO)"""
    return jsonify({
        'error': 'Función en desarrollo',
        'mensaje': 'La comparación automática estará disponible próximamente'
    }), 501


# ========== ENDPOINT: SUGERENCIAS DE BÚSQUEDA ==========
@app.route('/sugerencias', methods=['GET'])
def obtener_sugerencias():
    """
    Retorna sugerencias de búsqueda basadas en el caché
    Endpoint ultra rápido para autocompletado
    
    Parámetros:
    - query: texto parcial (ej: "pa" → "pan", "pan lactal", "pan rallado")
    - supermercado: opcional, filtrar por supermercado
    - limit: máximo de sugerencias (default 10)
    
    Ejemplo: /sugerencias?query=pa&supermercado=lagallega&limit=10
    """
    try:
        query = request.args.get('query', '').lower().strip()
        supermercado = request.args.get('supermercado', '').lower()
        limit = int(request.args.get('limit', 10))
        
        if not query or len(query) < 2:
            return jsonify({'sugerencias': []})
        
        from cache_manager import cache_manager
        sugerencias = set()
        
        # Buscar en caché con palabra completa (word boundary)
        supermercados_buscar = [supermercado] if supermercado else ['carrefour', 'dia', 'lareina', 'lagallega']
        
        for super_key in supermercados_buscar:
            if super_key not in cache_manager.cache['productos']:
                continue
            
            for nombre_producto in cache_manager.cache['productos'][super_key].keys():
                nombre_lower = ' ' + nombre_producto.lower() + ' '
                
                # Para autocomplete: buscar si el query está al inicio de cualquier palabra
                # "pa" → "pan", "pan lactal", "bizcochos de pan"
                # "du" → "dulce de leche", "dulce"
                if ' ' + query in nombre_lower:
                    # Agregar el nombre completo como sugerencia
                    sugerencias.add(nombre_producto)
                    if len(sugerencias) >= limit * 2:  # Buscar el doble y luego limitar
                        break
        
        # Convertir a lista y ordenar por relevancia
        sugerencias_lista = sorted(list(sugerencias), key=lambda x: (
            0 if x.lower().startswith(query) else 1,  # Primero los que empiezan con query
            len(x),  # Luego los más cortos
            x.lower()  # Finalmente alfabético
        ))[:limit]
        
        return jsonify({
            'query': query,
            'sugerencias': sugerencias_lista,
            'total': len(sugerencias_lista)
        })
        
    except Exception as e:
        print(f"❌ Error en sugerencias: {e}")
        return jsonify({'sugerencias': []}), 500


# ========== ENDPOINT: ESTADÍSTICAS DE CACHÉ ==========
@app.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Retorna estadísticas del caché de productos"""
    from cache_manager import cache_manager
    stats = cache_manager.obtener_estadisticas()
    return jsonify({
        'status': 'success',
        'cache': stats,
        'last_update': cache_manager.cache.get('last_update')
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("💰 MI LISTA DE PRECIOS - API SERVER")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("🛒 Supermercados: Carrefour, Día %, La Reina, La Gallega")
    print("📱 Compatible con app Android Mi Lista de Precios")
    print("🔍 Buscar: /products?query=PRODUCTO&supermercado=SUPER")
    print("🛒 Lista: /lista-compras (GET/POST/DELETE)")
    print("📊 Caché: /cache/stats")
    print("⚡ Sistema de caché activado para búsquedas instantáneas")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)