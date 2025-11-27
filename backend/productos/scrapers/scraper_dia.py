#!/usr/bin/env python3
"""
Scraper para supermercado Día % con 122 categorías
Utiliza la API de búsqueda de productos de Día Argentina
"""

from .base_scraper import BaseScraper
from typing import List, Dict
import requests
import json
import sys
import os

# Importar cache_manager desde backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from cache_manager import cache_manager

class ScraperDia(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://diaonline.supermercadosdia.com.ar",
            supermercado_nombre="Día %"
        )
        # API endpoint para búsqueda de productos
        self.api_url = "https://diaonline.supermercadosdia.com.ar/api/catalog_system/pub/products/search"
        self._precargando = False  # Flag para evitar recursión infinita
        
        # 122 categorías extraídas del árbol completo de Día
        # Similar a La Reina (212 cats) y La Gallega (136 cats)
        self.categorias = [
            1, 2, 16, 21, 25, 36, 42, 48, 53, 54,
            57, 63, 68, 71, 72, 76, 80, 81, 89, 95,
            103, 110, 121, 122, 132, 139, 146, 148, 154, 159,
            164, 165, 169, 172, 178, 182, 185, 193, 199, 200,
            201, 207, 209, 212, 213, 214, 215, 216, 217, 223,
            228, 233, 244, 248, 252, 256, 257, 265, 270, 276,
            280, 282, 283, 293, 297, 304, 308, 312, 321, 329,
            334, 335, 336, 337, 338, 339, 340, 344, 350, 354,
            359, 362, 366, 367, 375, 377, 378, 385, 396, 431,
            432, 436, 438, 439, 440, 441, 442, 444, 448, 450,
            461, 462, 10017, 10020, 10030, 10045, 10058, 10064, 10081, 10086,
            10098, 10099, 10110, 10113, 10119, 10121, 10123, 10128, 10132, 10133,
            10136, 10146,
        ]
        
    def _auto_precargar(self):
        """Precarga automática usando el método buscar_productos() que YA FUNCIONA"""
        print("")
        print("="*80)
        print("🚀 AUTOPRECARGA: Llenando caché de Día % con búsquedas reales...")
        print("="*80)
        print("⚠️  Este proceso tarda 3-5 minutos (usa búsquedas normales que funcionan)")
        print("⚠️  El caché se llena progresivamente, no necesita todo desde el inicio")
        print("")
        
        print(f"📊 Buscando productos comunes para llenar caché inicial...")
        print("")
        
        total_agregados = 0
        from time import sleep
        
        # Palabras clave que la gente realmente busca
        queries = [
            'leche', 'pan', 'yogur', 'queso', 'manteca', 'dulce de leche',
            'aceite', 'arroz', 'fideos', 'harina', 'azucar', 'sal',
            'cafe', 'te', 'mate', 'yerba', 'galletas', 'cerveza',
            'agua', 'gaseosa', 'jugo', 'vino', 'carne', 'pollo'
        ]
        
        for idx, palabra in enumerate(queries, 1):
            try:
                print(f"[{idx}/{len(queries)}] Buscando '{palabra}'...", end=" ", flush=True)
                
                # Usar el método buscar_productos() que YA FUNCIONA
                # Este método maneja la API correctamente y ya cachea automáticamente
                productos = self.buscar_productos(palabra)
                
                if productos:
                    # Los productos ya están cacheados por buscar_productos()
                    print(f"✅ {len(productos)} productos")
                    total_agregados += len(productos)
                else:
                    print(f"⚠️ Sin resultados")
                
                # Guardar cada 5 búsquedas
                if idx % 5 == 0:
                    cache_manager.guardar_cache()
                    print(f"   💾 Caché guardado")
                
                sleep(0.3)  # Pausa para no saturar la API
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        cache_manager.guardar_cache()
        print("")
        print("="*80)
        print(f"✅ AUTOPRECARGA COMPLETADA: ~{total_agregados} productos guardados")
        print("="*80)
        print("")
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Búsqueda RÁPIDA en Día con caché
        1. Busca en caché primero (instantáneo)
        2. Si catálogo completo precargado (>500), usa solo caché
        3. Si < 20 productos, busca en web
        """
        
        # Inicializar variable para evitar error de scope
        productos_cache = []
        
        # Si estamos precargando, saltar toda la lógica de caché y autoprecarga
        if not self._precargando:
            # PASO 1: Buscar en caché
            print(f"[Día %] Buscando '{query}'...")
            productos_cache = cache_manager.buscar_producto('dia', query)
            print(f"💾 {len(productos_cache)} productos en caché")
            
            # Si tenemos el catálogo completo precargado, usar solo caché
            total_en_cache = len(cache_manager.cache['productos'].get('dia', {}))
            
            # Si el caché está vacío o muy pequeño, hacer autoprecarga (evitar recursión)
            if total_en_cache < 100:
                print(f"⚠️  Caché insuficiente ({total_en_cache} productos), iniciando autoprecarga...")
                self._precargando = True
                self._auto_precargar()
                self._precargando = False
                # Volver a buscar después de precargar
                productos_cache = cache_manager.buscar_producto('dia', query)
                total_en_cache = len(cache_manager.cache['productos'].get('dia', {}))
            
            if total_en_cache > 500:
                print(f"⚡ Usando caché completo precargado ({total_en_cache} productos totales) - búsqueda instantánea")
                return self._formatear_productos_cache(productos_cache)
            
            if len(productos_cache) >= 20:
                print(f"⚡ Suficientes en caché, retornando")
                return self._formatear_productos_cache(productos_cache)
        
        # PASO 2: Buscar en web
        print(f"🌐 Buscando más en web...")
        productos_dict = {}  # Usar dict para evitar duplicados por nombre
        
        try:
            # Preparar queries: orden inverso para multi-palabra
            palabras = query.strip().split()
            queries_a_buscar = []
            
            if len(palabras) > 1:
                queries_a_buscar.extend(reversed(palabras))
            else:
                queries_a_buscar.append(query.strip())
            
            print(f"[Día %] Búsqueda rápida: '{query}'")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': self.base_url
            }
            
            # Buscar con cada query (SIN iterar categorías)
            for query_api in queries_a_buscar:
                try:
                    # Búsqueda DIRECTA = MÁS RÁPIDO
                    params = {
                        'ft': query_api,
                        '_from': 0,
                        '_to': 19  # 20 productos por query
                    }
                    
                    response = requests.get(
                        self.api_url,
                        params=params,
                        headers=headers,
                        timeout=5  # Timeout corto
                    )
                    
                    if response.status_code not in [200, 206]:
                        continue
                    
                    data = response.json()
                    if not data:
                        continue
                    
                    # Procesar productos
                    for item in data:
                        try:
                            nombre = item.get('productName', '')
                            if not nombre or nombre in productos_dict:
                                continue
                            
                            items = item.get('items', [])
                            if not items:
                                continue
                            
                            sellers = items[0].get('sellers', [])
                            if not sellers:
                                continue
                            
                            precio = float(sellers[0].get('commertialOffer', {}).get('Price', 0))
                            
                            # Imagen
                            imagen_url = None
                            images = items[0].get('images', [])
                            if images:
                                imagen_url = images[0].get('imageUrl', '')
                            
                            if precio > 0:
                                producto_url = item.get('link', self.base_url)
                                productos_dict[nombre] = {
                                    'nombre': nombre,
                                    'precio': precio,
                                    'supermercado': self.supermercado_nombre,
                                    'url': producto_url,
                                    'imagen': imagen_url
                                }
                                
                                # Guardar en caché
                                cache_manager.agregar_producto(
                                    supermercado='dia',
                                    nombre=nombre,
                                    categoria='',
                                    precio=precio,
                                    url=producto_url,
                                    imagen_url=imagen_url
                                )
                        
                        except (KeyError, IndexError, ValueError):
                            continue
                
                except Exception:
                    continue
            
        except Exception as e:
            print(f"[Día %] Error en búsqueda: {e}")
        
        # Guardar caché
        cache_manager.guardar_cache()
        
        productos_lista = list(productos_dict.values())
        print(f"✅ Scraping: {len(productos_lista)} productos nuevos")
        
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
        return [{
            'nombre': p['nombre'],
            'precio': p['precio'],
            'supermercado': self.supermercado_nombre,
            'imagen': p.get('imagen_url'),
            'url': p['url']
        } for p in productos_cache]
