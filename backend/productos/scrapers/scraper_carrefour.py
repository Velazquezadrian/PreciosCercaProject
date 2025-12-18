# Scraper para Carrefour usando API VTEX con 148 categorías
from .base_scraper import BaseScraper
from typing import List, Dict
import json
import sys
import os

# Importar cache_manager desde backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from cache_manager import cache_manager

class ScraperCarrefour(BaseScraper):
    def __init__(self):
        # VTEX API endpoint para búsquedas
        super().__init__(
            base_url="https://www.carrefour.com.ar",
            supermercado_nombre="Carrefour"
        )
        self.api_search_url = "https://www.carrefour.com.ar/api/catalog_system/pub/products/search"
        self._precargando = False  # Flag para evitar recursión infinita
        
        # 148 categorías extraídas del árbol completo de Carrefour
        # Similar a La Reina (212 cats) y La Gallega (136 cats)
        self.categorias = [
            1, 3, 4, 7, 11, 15, 20, 25, 31, 42,
            48, 56, 62, 71, 72, 88, 138, 148, 157, 161,
            162, 168, 172, 176, 183, 190, 195, 199, 206, 208,
            214, 222, 223, 229, 232, 233, 238, 242, 246, 250,
            255, 256, 257, 262, 266, 273, 277, 283, 286, 290,
            291, 292, 293, 299, 302, 303, 304, 305, 306, 307,
            308, 309, 310, 318, 321, 322, 323, 324, 326, 327,
            329, 330, 331, 332, 333, 334, 336, 337, 340, 344,
            345, 346, 347, 348, 349, 350, 352, 356, 358, 359,
            360, 367, 376, 377, 384, 385, 386, 387, 390, 394,
            402, 403, 412, 418, 422, 427, 435, 438, 443, 444,
            445, 451, 452, 453, 458, 462, 466, 467, 468, 469,
            470, 471, 472, 473, 474, 475, 498, 499, 514, 525,
            564, 600, 605, 606, 607, 608, 635, 636, 637, 640,
            650, 658, 665, 666, 667, 668, 669, 686,
        ]
    
    def _auto_precargar(self):
        """Precarga COMPLETA de todos los productos de Carrefour usando paginación"""
        print("")
        print("="*80)
        print("🚀 AUTOPRECARGA COMPLETA: Descargando TODO el catálogo de Carrefour...")
        print("="*80)
        print("⚠️  Carrefour tiene ~90,000 productos, esto tardará 15-20 minutos")
        print("")
        
        total_agregados = 0
        productos_unicos = set()
        from time import sleep
        import requests
        
        # Configuración de paginación
        PAGE_SIZE = 50  # Productos por request (máximo de VTEX)
        MAX_PRODUCTOS = 90000  # Límite seguro
        
        try:
            print(f"📊 Descargando productos de Carrefour por páginas de {PAGE_SIZE}...")
            print("")
            
            current_from = 0
            
            while current_from < MAX_PRODUCTOS:
                try:
                    current_to = current_from + PAGE_SIZE - 1
                    
                    # Request a la API VTEX sin filtros (todos los productos)
                    params = {
                        '_from': current_from,
                        '_to': current_to,
                        'O': 'OrderByTopSaleDESC'  # Ordenar por más vendidos
                    }
                    
                    response = self.session.get(
                        self.api_search_url,
                        params=params,
                        timeout=30
                    )
                    
                    if response.status_code not in [200, 206]:
                        print(f"❌ Error HTTP {response.status_code} en offset {current_from}")
                        break
                    
                    productos_json = response.json()
                    
                    if not productos_json or len(productos_json) == 0:
                        print(f"✅ Fin del catálogo en offset {current_from}")
                        break
                    
                    # Procesar productos de esta página
                    productos_pagina = 0
                    for producto_vtex in productos_json:
                        try:
                            nombre = producto_vtex.get('productName', '').strip()
                            if not nombre or nombre in productos_unicos:
                                continue
                            
                            items = producto_vtex.get('items', [])
                            if not items:
                                continue
                            
                            sellers = items[0].get('sellers', [])
                            if not sellers:
                                continue
                            
                            precio = sellers[0].get('commertialOffer', {}).get('Price', 0)
                            if precio <= 0:
                                continue
                            
                            # Imagen
                            imagen_url = None
                            images = items[0].get('images', [])
                            if images:
                                imagen_url = images[0].get('imageUrl', '')
                            
                            # URL del producto
                            producto_url = f"{self.base_url}/{producto_vtex.get('linkText', '')}/p"
                            
                            # Agregar al caché
                            cache_manager.agregar_producto(
                                supermercado='carrefour',
                                nombre=nombre,
                                categoria='',
                                precio=float(precio),
                                url=producto_url,
                                imagen_url=imagen_url
                            )
                            
                            productos_unicos.add(nombre)
                            productos_pagina += 1
                            total_agregados += 1
                            
                        except Exception as e:
                            continue
                    
                    # Progress update
                    print(f"[Offset {current_from:6d}-{current_to:6d}] ✅ {productos_pagina:2d} productos | Total: {total_agregados:5d}", flush=True)
                    
                    # Guardar caché cada 500 productos
                    if total_agregados % 500 == 0:
                        cache_manager.guardar_cache()
                        print(f"   💾 Caché guardado ({total_agregados} productos)")
                    
                    # Avanzar a la siguiente página
                    current_from += PAGE_SIZE
                    
                    # Pausa para no saturar la API
                    sleep(0.2)
                    
                except Exception as e:
                    print(f"❌ Error en offset {current_from}: {e}")
                    current_from += PAGE_SIZE
                    continue
        
        except KeyboardInterrupt:
            print("\n⚠️ Precarga interrumpida por el usuario")
        
        except Exception as e:
            print(f"\n❌ Error fatal: {e}")
        
        finally:
            # Guardar caché final
            cache_manager.guardar_cache()
            print("")
            print("="*80)
            print(f"✅ AUTOPRECARGA COMPLETADA: {total_agregados} productos guardados")
            print("="*80)
            print("")
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Búsqueda RÁPIDA en Carrefour con caché
        1. Busca en caché primero (instantáneo)
        2. Si caché completo (> 500 productos), usar solo caché
        3. Si no, buscar en web
        """
        
        # Inicializar variable para evitar error de scope
        productos_cache = []
        
        # Si estamos precargando, saltar toda la lógica de caché y autoprecarga
        if not self._precargando:
            # PASO 1: Buscar en caché
            print(f"[Carrefour] Buscando '{query}'...")
            productos_cache = cache_manager.buscar_producto('carrefour', query)
            print(f"💾 {len(productos_cache)} productos en caché")
            
            # Si el caché tiene un catálogo completo, confiar en él
            total_en_cache = len(cache_manager.cache['productos'].get('carrefour', {}))
            print(f"💾 Total productos en caché de Carrefour: {total_en_cache}")
            
            # Si el caché está vacío o muy pequeño, hacer autoprecarga (evitar recursión)
            if total_en_cache < 100:
                print(f"⚠️  Caché insuficiente ({total_en_cache} productos), iniciando autoprecarga...")
                self._precargando = True
                self._auto_precargar()
                self._precargando = False
                # Volver a buscar después de precargar
                productos_cache = cache_manager.buscar_producto('carrefour', query)
                total_en_cache = len(cache_manager.cache['productos'].get('carrefour', {}))
            
            if total_en_cache > 500:
                print(f"⚡ Usando caché completo precargado (búsqueda instantánea)")
                return self._formatear_productos_cache(productos_cache)
            
            # Fallback: buscar en web si caché incompleto
            if len(productos_cache) >= 20:
                print(f"⚡ Suficientes en caché, retornando")
                return self._formatear_productos_cache(productos_cache)
        
        # PASO 2: Buscar en web
        print(f"🌐 Buscando más en web...")
        productos_dict = {}  # Usar dict para evitar duplicados por nombre
        
        try:
            # Preparar queries: palabras en orden inverso para multi-palabra
            palabras = query.strip().split()
            queries_a_buscar = []
            
            if len(palabras) > 1:
                # Búsqueda multi-palabra: orden inverso (específico primero)
                queries_a_buscar.extend(reversed(palabras))
            else:
                queries_a_buscar.append(query.strip())
            
            print(f"[Carrefour] Búsqueda rápida: '{query}'")
            
            # Buscar con cada query (SIN iterar categorías)
            for query_api in queries_a_buscar:
                try:
                    # Búsqueda DIRECTA sin filtro de categoría = MÁS RÁPIDO
                    params = {
                        'ft': query_api,
                        '_from': 0,
                        '_to': 19  # Solo 20 productos por query
                    }
                    
                    response = self.session.get(
                        self.api_search_url, 
                        params=params, 
                        timeout=5  # Timeout más corto
                    )
                    
                    if response.status_code not in [200, 206]:
                        continue
                    
                    productos_json = response.json()
                    
                    if not productos_json:
                        continue
                    
                    # Procesar productos
                    for producto_vtex in productos_json:
                        try:
                            nombre = producto_vtex.get('productName', '')
                            if not nombre or nombre in productos_dict:
                                continue
                            
                            items = producto_vtex.get('items', [])
                            if not items:
                                continue
                            
                            sellers = items[0].get('sellers', [])
                            if not sellers:
                                continue
                            
                            precio = sellers[0].get('commertialOffer', {}).get('Price', 0)
                            
                            # Imagen
                            imagen_url = None
                            images = items[0].get('images', [])
                            if images:
                                imagen_url = images[0].get('imageUrl', '')
                            
                            if precio > 0:
                                producto_url = f"{self.base_url}/{producto_vtex.get('linkText', '')}/p"
                                productos_dict[nombre] = {
                                    'nombre': nombre.strip(),
                                    'precio': float(precio),
                                    'supermercado': self.supermercado_nombre,
                                    'url': producto_url,
                                    'imagen': imagen_url
                                }
                                
                                # Guardar en caché
                                cache_manager.agregar_producto(
                                    supermercado='carrefour',
                                    nombre=nombre.strip(),
                                    categoria='',  # Carrefour no usa categorías en este scraper
                                    precio=float(precio),
                                    url=producto_url,
                                    imagen_url=imagen_url
                                )
                        
                        except Exception:
                            continue
                
                except Exception:
                    continue
            
        except Exception as e:
            print(f"[Carrefour] Error en búsqueda: {e}")
        
        # Guardar caché
        cache_manager.guardar_cache()
        
        productos_lista = list(productos_dict.values())
        print(f"✅ Scraping completado: {len(productos_lista)} productos nuevos")
        
        # COMBINAR con caché
        if productos_cache:
            print(f"   Combinando con {len(productos_cache)} del caché...")
            nombres_scraping = {p['nombre'].lower() for p in productos_lista}
            
            for prod_cache in productos_cache:
                if prod_cache['nombre'].lower() not in nombres_scraping:
                    productos_lista.append({
                        'nombre': prod_cache['nombre'],
                        'precio': prod_cache['precio'],
                        'supermercado': self.supermercado_nombre,
                        'imagen': prod_cache.get('imagen_url'),
                        'url': prod_cache['url']
                    })
        
        print(f"✅ Total retornados: {len(productos_lista)}")
        return productos_lista
    
    def _formatear_productos_cache(self, productos_cache):
        """Convierte productos del caché al formato esperado"""
        productos_formateados = []
        
        for prod in productos_cache:
            productos_formateados.append({
                'nombre': prod['nombre'],
                'precio': prod['precio'],
                'supermercado': self.supermercado_nombre,
                'imagen': prod.get('imagen_url'),
                'url': prod['url']
            })
        
        return productos_formateados