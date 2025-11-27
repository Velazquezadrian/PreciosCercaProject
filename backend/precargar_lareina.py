"""
Script para precargar TODO el catálogo de La Reina en el caché
HTML Scraping - Moderado (3-5 minutos)
"""

import sys
import os
from time import sleep

sys.path.insert(0, os.path.dirname(__file__))

from cache_manager import cache_manager
from productos.scrapers.scraper_lareina import ScraperLaReina

def precargar_lareina():
    print("="*80)
    print("🚀 PRECARGA COMPLETA DEL CATÁLOGO DE LA REINA")
    print("="*80)
    print()
    print("⚠️  Este proceso puede tardar 3-5 minutos")
    print("⚠️  Descargará productos de las 9 categorías principales")
    print()
    input("Presiona ENTER para continuar...")
    print()
    
    scraper = ScraperLaReina()
    
    # Las 9 categorías de La Reina
    categorias = scraper.categorias
    
    print(f"📊 Categorías a procesar: {len(categorias)}")
    print()
    
    total_productos = 0
    categorias_procesadas = 0
    errores = 0
    
    for i, cat_url in enumerate(categorias, 1):
        try:
            # Extraer nombre de categoría de la URL
            cat_name = cat_url.split('/')[-1] if '/' in cat_url else cat_url
            print(f"[{i}/{len(categorias)}] Procesando '{cat_name}'...", end=" ", flush=True)
            
            url = f"{scraper.base_url}/{cat_url}"
            soup = scraper.hacer_request(url)
            
            if not soup:
                print("❌ Error al cargar")
                errores += 1
                continue
            
            # Buscar productos
            productos_div = soup.find_all('div', class_='product')
            
            productos_guardados = 0
            for prod_div in productos_div:
                try:
                    # Extraer nombre
                    nombre_elem = prod_div.find('h3')
                    if not nombre_elem:
                        continue
                    nombre = nombre_elem.get_text(strip=True)
                    
                    # Verificar si ya existe
                    if nombre in cache_manager.cache['productos']['lareina']:
                        continue
                    
                    # Extraer precio
                    import re
                    precio_match = re.search(r'\$\s*([\d.,]+)', prod_div.get_text())
                    if not precio_match:
                        continue
                    
                    try:
                        precio = scraper.limpiar_precio(precio_match.group(0))
                    except:
                        continue
                    
                    # Extraer imagen
                    img_elem = prod_div.find('img')
                    imagen_url = None
                    if img_elem:
                        img_src = img_elem.get('src', '')
                        if img_src:
                            if img_src.startswith('http'):
                                imagen_url = img_src
                            elif img_src.startswith('/'):
                                imagen_url = f"{scraper.base_url}{img_src}"
                            else:
                                imagen_url = f"{scraper.base_url}/{img_src}"
                    
                    # Extraer URL
                    link = prod_div.find('a', href=True)
                    producto_url = scraper.base_url
                    if link:
                        href = link.get('href', '')
                        if href.startswith('http'):
                            producto_url = href
                        elif href.startswith('/'):
                            producto_url = f"{scraper.base_url}{href}"
                        else:
                            producto_url = f"{scraper.base_url}/{href}"
                    
                    cache_manager.agregar_producto(
                        supermercado='lareina',
                        nombre=nombre,
                        categoria=cat_name,
                        precio=precio,
                        url=producto_url,
                        imagen_url=imagen_url
                    )
                    
                    productos_guardados += 1
                    total_productos += 1
                    
                except Exception as e:
                    continue
            
            print(f"✅ {productos_guardados} productos nuevos")
            categorias_procesadas += 1
            
            # Guardar cada 3 categorías
            if i % 3 == 0:
                cache_manager.guardar_cache()
                print(f"   💾 Caché guardado ({total_productos} productos totales)")
            
            sleep(0.5)  # Pausa entre categorías
            
        except Exception as e:
            print(f"❌ Error: {e}")
            errores += 1
    
    cache_manager.guardar_cache()
    
    print()
    print("="*80)
    print("✅ PRECARGA DE LA REINA FINALIZADA")
    print("="*80)
    print(f"📊 Categorías procesadas: {categorias_procesadas}/{len(categorias)}")
    print(f"📦 Total de productos guardados: {total_productos}")
    print(f"❌ Errores: {errores}")
    print()
    print("🚀 Búsquedas en La Reina ahora son instantáneas!")
    print()

if __name__ == "__main__":
    precargar_lareina()
