#!/usr/bin/env python3
"""
Scraper para Coto Digital
Utiliza HTML scraping con BeautifulSoup
"""

from .base_scraper import BaseScraper
from typing import List, Dict
from bs4 import BeautifulSoup
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
        self.search_url = "https://www.cotodigital.com.ar/sitios/cdigi/browse"
        self._precargando = False
        
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
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Búsqueda en Coto Digital
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
        
        # Buscar en web
        print(f"🌐 Buscando más en web...")
        productos_dict = {}
        
        try:
            # Preparar queries
            palabras = query.strip().split()
            queries_a_buscar = []
            
            if len(palabras) > 1:
                queries_a_buscar.extend(reversed(palabras))
            else:
                queries_a_buscar.append(query.strip())
            
            print(f"[Coto] Búsqueda: '{query}'")
            
            for query_api in queries_a_buscar[:1]:  # Solo primera query
                try:
                    params = {
                        '_Ntt': query_api,
                        '_Nrpp': 20  # Máximo 20 productos
                    }
                    
                    response = self.session.get(
                        self.search_url,
                        params=params,
                        timeout=10
                    )
                    
                    if response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Buscar productos en el HTML
                    # Coto usa diferentes estructuras, intentar varios selectores
                    productos_html = soup.find_all('div', class_='product_info_container')
                    
                    if not productos_html:
                        productos_html = soup.find_all('article', class_='product')
                    
                    if not productos_html:
                        productos_html = soup.find_all('div', class_='item')
                    
                    for producto_html in productos_html[:20]:
                        try:
                            # Extraer nombre
                            nombre_elem = producto_html.find(['h3', 'h4', 'span'], class_=lambda x: x and ('name' in x.lower() or 'title' in x.lower() or 'description' in x.lower()))
                            if not nombre_elem:
                                nombre_elem = producto_html.find('a', class_=lambda x: x and 'product' in x.lower())
                            
                            if not nombre_elem:
                                continue
                            
                            nombre = nombre_elem.get_text(strip=True)
                            if not nombre or nombre in productos_dict:
                                continue
                            
                            # Extraer precio
                            precio = 0
                            precio_elem = producto_html.find(['span', 'div'], class_=lambda x: x and ('price' in x.lower() or 'precio' in x.lower()))
                            
                            if precio_elem:
                                precio_text = precio_elem.get_text(strip=True)
                                # Limpiar formato: "$1.234,56" -> 1234.56
                                precio_text = precio_text.replace('$', '').replace('.', '').replace(',', '.').strip()
                                try:
                                    precio = float(precio_text)
                                except:
                                    continue
                            
                            if precio <= 0:
                                continue
                            
                            # Extraer imagen
                            imagen_url = None
                            img_elem = producto_html.find('img')
                            if img_elem:
                                imagen_url = img_elem.get('src') or img_elem.get('data-src')
                                if imagen_url and not imagen_url.startswith('http'):
                                    imagen_url = self.base_url + imagen_url
                            
                            # Extraer URL
                            url_elem = producto_html.find('a', href=True)
                            producto_url = self.base_url
                            if url_elem:
                                href = url_elem['href']
                                if not href.startswith('http'):
                                    producto_url = self.base_url + href
                                else:
                                    producto_url = href
                            
                            productos_dict[nombre] = {
                                'nombre': nombre,
                                'precio': float(precio),
                                'supermercado': self.supermercado_nombre,
                                'url': producto_url,
                                'imagen': imagen_url
                            }
                            
                            # Guardar en caché
                            cache_manager.agregar_producto(
                                supermercado='coto',
                                nombre=nombre,
                                categoria='',
                                precio=float(precio),
                                url=producto_url,
                                imagen_url=imagen_url
                            )
                        
                        except Exception:
                            continue
                
                except Exception:
                    continue
            
        except Exception as e:
            print(f"[Coto] Error en búsqueda: {e}")
        
        cache_manager.guardar_cache()
        
        productos_lista = list(productos_dict.values())
        print(f"✅ Scraping completado: {len(productos_lista)} productos nuevos")
        
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
