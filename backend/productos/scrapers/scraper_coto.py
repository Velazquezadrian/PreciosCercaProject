#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper para Coto Digital
Utiliza API JSON (Oracle Endeca) - FUNCIONAL
"""

from .base_scraper import BaseScraper
from typing import List, Dict
import json
import sys
import os

# Importar cache_manager desde backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from cache_manager import cache_manager

class ScraperCoto(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://www.cotodigital.com.ar",
            supermercado_nombre="Coto"
        )
        # API JSON de Coto (Oracle Endeca)
        self.search_url = "https://www.cotodigital.com.ar/sitios/cdigi/browse"
        self._precargando = False
        
        # Headers completos para bypasser Fortigate
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'identity',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Connection': 'keep-alive'
        })
        
        # Cargar página principal para obtener cookies y bypass
        try:
            from time import sleep
            print("[Coto] Inicializando sesión...")
            response = self.session.get(self.base_url, timeout=15)
            sleep(2)  # Esperar 2 segundos como navegador real
            print(f"[Coto] Sesión lista (cookies: {len(self.session.cookies)})")
        except Exception as e:
            print(f"[Coto] Advertencia al inicializar: {e}")
        
    def _auto_precargar(self):
        """Precarga automática con búsquedas de términos comunes"""
        print("")
        print("="*80)
        print("🚀 AUTOPRECARGA: Coto Digital con búsquedas...")
        print("="*80)
        
        total_agregados = 0
        from time import sleep
        
        queries = [
            'leche', 'yogur', 'queso', 'pan', 'aceite', 'arroz', 
            'fideos', 'azucar', 'cafe', 'yerba', 'gaseosa', 'cerveza'
        ]
        
        for idx, palabra in enumerate(queries, 1):
            try:
                print(f"[{idx}/{len(queries)}] Buscando '{palabra}'...", end=" ", flush=True)
                productos = self.buscar_productos(palabra)
                
                if productos:
                    print(f"✅ {len(productos)} productos")
                    total_agregados += len(productos)
                else:
                    print(f"⚠️ Sin resultados")
                
                if idx % 5 == 0:
                    cache_manager.guardar_cache()
                    print(f"   💾 Caché guardado")
                
                sleep(0.3)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        cache_manager.guardar_cache()
        print("")
        print("="*80)
        print(f"✅ AUTOPRECARGA COMPLETADA: ~{total_agregados} productos guardados")
        print("="*80)
        print("")
    
    def _obtener_pagina(self, query: str = None, offset: int = 0, limit: int = 72) -> List[Dict]:
        """
        Obtiene una página de productos de Coto
        
        Args:
            query: Término de búsqueda (None para catálogo completo)
            offset: Número de registro inicial (para paginación)
            limit: Cantidad de productos a retornar
        
        Returns:
            Lista de productos en formato dict
        """
        try:
            # ✅ IMPORTANTE: Cargar página principal primero para obtener cookies
            if not self.session.cookies:
                self.session.get(self.base_url, timeout=10)
            
            # Parámetros para Oracle Endeca
            params = {
                '_Nrpp': limit,      # Registros por página
                'No': offset,        # Offset para paginación
                'format': 'json'     # Retornar JSON
            }
            
            # Agregar búsqueda si se especifica
            if query:
                params['_Ntt'] = query
            
            response = self.session.get(
                self.search_url,
                params=params,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"❌ Error HTTP: {response.status_code}")
                return []
            
            # Parsear JSON
            data = response.json()
            
            # Navegar estructura compleja de Oracle Endeca
            if 'contents' not in data or len(data['contents']) == 0:
                return []
            
            main_content_list = data['contents'][0].get('MainContent', [])
            if len(main_content_list) < 2:
                return []
            
            content_slot = main_content_list[1]
            if '@type' not in content_slot or content_slot['@type'] != 'ContentSlot-Main':
                return []
            
            inner_contents = content_slot.get('contents', [])
            if len(inner_contents) == 0:
                return []
            
            results_list = inner_contents[0]
            if 'records' not in results_list:
                return []
            
            records = results_list['records']
            if not records or len(records) == 0:
                return []
            
            # Procesar productos
            productos = []
            for record in records:
                try:
                    sub_records = record.get('records', [])
                    if not sub_records or len(sub_records) == 0:
                        continue
                    
                    sku_record = sub_records[0]
                    attrs = sku_record.get('attributes', {})
                    
                    # Extraer nombre
                    nombre_lista = attrs.get('product.displayName') or attrs.get('sku.displayName')
                    if not nombre_lista or len(nombre_lista) == 0:
                        continue
                    nombre = nombre_lista[0]
                    
                    # Extraer precio
                    precio = 0
                    dto_price_lista = attrs.get('sku.dtoPrice', [])
                    if dto_price_lista and len(dto_price_lista) > 0:
                        try:
                            dto_json = json.loads(dto_price_lista[0])
                            precio = float(dto_json.get('precio') or dto_json.get('precioLista', 0))
                        except:
                            pass
                    
                    if precio <= 0:
                        active_price_lista = attrs.get('sku.activePrice', [])
                        if active_price_lista:
                            try:
                                precio = float(active_price_lista[0])
                            except:
                                pass
                    
                    if precio <= 0:
                        continue
                    
                    # Extraer imagen
                    imagen_url = None
                    imagen_lista = attrs.get('product.mediumImage.url') or attrs.get('product.smallImage.url')
                    if imagen_lista and len(imagen_lista) > 0:
                        imagen_url = imagen_lista[0]
                        if not imagen_url.startswith('http'):
                            imagen_url = self.base_url + imagen_url
                    
                    # Extraer URL del producto
                    detail_action = sku_record.get('detailsAction', {})
                    record_state = detail_action.get('recordState', '')
                    producto_url = self.base_url + '/sitios/cdigi' + record_state if record_state else self.base_url
                    
                    productos.append({
                        'nombre': nombre,
                        'precio': float(precio),
                        'supermercado': self.supermercado_nombre,
                        'url': producto_url,
                        'imagen': imagen_url
                    })
                    
                except Exception as e:
                    continue
            
            return productos
            
        except Exception as e:
            print(f"❌ Error obteniendo página: {e}")
            return []
    
    def buscar_productos(self, query: str, max_paginas: int = 1) -> List[Dict]:
        """
        Búsqueda en Coto Digital usando API JSON (Oracle Endeca)
        
        Args:
            query: Término de búsqueda
            max_paginas: Número máximo de páginas a obtener (1-5)
        
        Returns:
            Lista de productos encontrados
        """
        productos_cache = []
        
        if not self._precargando:
            print(f"[Coto] Buscando '{query}'...")
            productos_cache = cache_manager.buscar_producto('coto', query)
            print(f"💾 {len(productos_cache)} productos en caché")
            
            total_en_cache = len(cache_manager.cache['productos'].get('coto', {}))
            print(f"💾 Total productos en caché de Coto: {total_en_cache}")
            
            if total_en_cache < 100:
                print(f"⚠️  Caché insuficiente ({total_en_cache} productos), iniciando autoprecarga...")
                self._precargando = True
                self._auto_precargar()
                self._precargando = False
                productos_cache = cache_manager.buscar_producto('coto', query)
                total_en_cache = len(cache_manager.cache['productos'].get('coto', {}))
            
            if total_en_cache > 500:
                print(f"⚡ Usando caché completo precargado")
                return self._formatear_productos_cache(productos_cache)
            
            if len(productos_cache) >= 20:
                print(f"⚡ Suficientes en caché, retornando")
                return self._formatear_productos_cache(productos_cache)
        
        # Buscar en API JSON con paginación
        print(f"🌐 Buscando en API JSON de Coto (hasta {max_paginas} páginas)...")
        productos_dict = {}
        
        # Preparar query (usar primera palabra)
        palabras = query.strip().split()
        query_api = palabras[0] if len(palabras) > 0 else query
        print(f"[Coto] Query API: '{query_api}'")
        
        # Obtener múltiples páginas
        for pagina in range(max_paginas):
            offset = pagina * 72
            print(f"   Página {pagina + 1}/{max_paginas} (offset {offset})...")
            
            productos_pagina = self._obtener_pagina(query=query_api, offset=offset, limit=72)
            
            if not productos_pagina:
                print(f"   ⚠️  Sin más productos")
                break
            
            print(f"   ✅ {len(productos_pagina)} productos")
            
            # Agregar al dict (evita duplicados)
            for prod in productos_pagina:
                if prod['nombre'] not in productos_dict:
                    productos_dict[prod['nombre']] = prod
                    
                    # Guardar en caché
                    cache_manager.agregar_producto(
                        supermercado='coto',
                        nombre=prod['nombre'],
                        categoria='',
                        precio=prod['precio'],
                        url=prod['url'],
                        imagen_url=prod['imagen']
                    )
            
            # Si obtuvimos menos de 72, no hay más páginas
            if len(productos_pagina) < 72:
                break
        
        cache_manager.guardar_cache()
        
        productos_lista = list(productos_dict.values())
        print(f"✅ API JSON completado: {len(productos_lista)} productos nuevos")
        
        # Combinar con caché
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
