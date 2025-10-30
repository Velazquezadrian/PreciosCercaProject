#!/usr/bin/env python3
"""
PreciosCerca - Servidor Principal
================================

Servidor Flask que proporciona una API REST para buscar productos y precios
en supermercados argentinos usando web scraping.

Actualmente soporta:
- Carrefour (API VTEX) ✅
- Día % (API REST) ✅

Autor: PreciosCerca Team
Fecha: Octubre 2025
"""

from flask import Flask, jsonify, request
import sys
import os

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 Inicializando PreciosCerca Server...")

try:
    from productos.scrapers.scraper_carrefour import ScraperCarrefour
    from productos.scrapers.scraper_dia import ScraperDia
    from productos.scrapers.sucursales_data import (
        encontrar_sucursal_mas_cercana, 
        obtener_sucursales,
        obtener_supermercados_cercanos,
        filtrar_sucursales_por_radio,
        detectar_ciudad_usuario,
        obtener_supermercados_por_ciudad
    )
    print("✅ Carrefour scraper cargado correctamente")
    print("✅ Día % scraper cargado correctamente")
    print("✅ Datos de sucursales cargados correctamente")
except Exception as e:
    print(f"❌ Error cargando scrapers: {e}")
    sys.exit(1)

app = Flask(__name__)

# Inicializar scrapers disponibles
# Por ahora solo La Gallega funcional
scrapers = {
    'lagallega': ScraperCarrefour(),  # Temporalmente usando Carrefour scraper para La Gallega
    # 'carrefour': ScraperCarrefour(),
    # 'dia': ScraperDia()
}

print(f"✅ {len(scrapers)} scraper(s) inicializado(s) - Solo La Gallega")

@app.route('/products', methods=['GET'])
def buscar_productos():
    """
    Endpoint principal para buscar productos.
    
    Parámetros:
    - query: término de búsqueda (ej: "leche", "pan", "jabón")
    
    Retorna JSON con estructura compatible con app Android:
    {
        "query": "leche",
        "total_encontrados": 50,
        "supermercados_consultados": ["Carrefour"],
        "productos_por_supermercado": {"Carrefour": 50},
        "resultados": [...]
    }
    """
    query = request.args.get('query', request.args.get('q', 'leche'))
    
    print(f"🔍 Búsqueda: '{query}'")
    
    try:
        todos_los_productos = []
        supermercados_consultados = []
        productos_por_supermercado = {}
        
        # Buscar en La Gallega (usando scraper de Carrefour temporalmente)
        print("  🔍 Buscando en La Gallega...")
        lagallega_productos = scrapers['lagallega'].buscar_productos(query)
        # Cambiar el nombre del supermercado en los resultados
        for prod in lagallega_productos:
            prod['supermercado'] = 'La Gallega'
        todos_los_productos.extend(lagallega_productos)
        supermercados_consultados.append('La Gallega')
        productos_por_supermercado['La Gallega'] = len(lagallega_productos)
        print(f"  ✅ La Gallega: {len(lagallega_productos)} productos")
        
        # Ordenar por precio (más barato primero)
        todos_los_productos.sort(key=lambda x: x['precio'])
        
        # Convertir al formato que espera la app Android
        resultados = []
        for producto in todos_los_productos:
            resultados.append({
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'supermercado': producto['supermercado'],
                'fecha': '2025-10-30',
                'relevancia': 1.0,
                'url': producto.get('url', '')  # Agregar URL del producto
            })
        
        print(f"✅ {len(resultados)} productos encontrados")
        
        # Respuesta en formato Android
        response = {
            'query': query,
            'total_encontrados': len(resultados),
            'supermercados_consultados': supermercados_consultados,
            'productos_por_supermercado': productos_por_supermercado,
            'resultados': resultados
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
    """
    Busca productos solo en supermercados con sucursales cercanas.
    Solo muestra productos de supermercados que tengan al menos una sucursal dentro del radio.
    Los productos se ordenan primero por supermercado (más cercano primero) y luego por precio.
    
    Parámetros:
    - query: término de búsqueda (ej: "leche")
    - lat: latitud del usuario
    - lng: longitud del usuario
    - radio: radio de búsqueda en km (opcional, default: 50)
    
    Retorna productos solo de supermercados que tengan sucursales cerca.
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
    """
    Encuentra la sucursal más cercana a la ubicación del usuario.
    
    Parámetros:
    - supermercado: nombre del supermercado (ej: "Carrefour", "Día %")
    - lat: latitud del usuario
    - lng: longitud del usuario
    
    Retorna JSON con información de la sucursal más cercana.
    """
    try:
        supermercado = request.args.get('supermercado', '')
        lat = float(request.args.get('lat', 0))
        lng = float(request.args.get('lng', 0))
        
        if not supermercado or lat == 0 or lng == 0:
            return jsonify({
                'error': 'Parámetros incompletos. Se requiere: supermercado, lat, lng'
            }), 400
        
        sucursal = encontrar_sucursal_mas_cercana(supermercado, lat, lng)
        
        if not sucursal:
            return jsonify({
                'error': f'No se encontraron sucursales para {supermercado}'
            }), 404
        
        # Agregar URL de Google Maps usando la DIRECCIÓN en lugar de coordenadas GPS
        # Esto asegura que Google Maps busque la dirección exacta en lugar de coordenadas aproximadas
        direccion_busqueda = f"{sucursal['nombre']}, {sucursal['direccion']}"
        direccion_codificada = direccion_busqueda.replace(' ', '+')
        sucursal['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={direccion_codificada}"
        
        return jsonify({
            'supermercado': supermercado,
            'sucursal': sucursal
        })
        
    except ValueError:
        return jsonify({
            'error': 'Latitud y longitud deben ser números válidos'
        }), 400
    except Exception as e:
        print(f"❌ Error buscando sucursal: {e}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/sucursales', methods=['GET'])
def listar_sucursales():
    """
    Lista todas las sucursales de un supermercado.
    
    Parámetros:
    - supermercado: nombre del supermercado (opcional, si no se envía devuelve todas)
    
    Retorna JSON con lista de sucursales.
    """
    try:
        supermercado = request.args.get('supermercado', '')
        
        if supermercado:
            sucursales = obtener_sucursales(supermercado)
            return jsonify({
                'supermercado': supermercado,
                'total': len(sucursales),
                'sucursales': sucursales
            })
        else:
            # Devolver todas las sucursales de todos los supermercados
            from productos.scrapers.sucursales_data import SUCURSALES
            return jsonify({
                'supermercados': list(SUCURSALES.keys()),
                'sucursales': SUCURSALES
            })
            
    except Exception as e:
        print(f"❌ Error listando sucursales: {e}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏪 PRECIOSCERCA SERVER - LA GALLEGA ROSARIO")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("🛒 Supermercados disponibles: La Gallega (Rosario)")
    print("📱 Compatible con app Android PreciosCerca")
    print("🔍 Endpoint: /products?query=PRODUCTO")
    print("📍 Endpoint cercanos: /products-cercanos?query=PRODUCTO&lat=LAT&lng=LNG&radio=KM")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)