"""
Script para precargar TODO el catálogo de La Gallega en el caché
Esto permite búsquedas instantáneas sin tener que scrapear cada vez
"""

import sys
import os
from time import sleep

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

from cache_manager import cache_manager
from productos.scrapers.scraper_lagallega import ScraperLaGallega

def precargar_catalogo_completo():
    """
    Precarga TODO el catálogo de La Gallega (todas las 136 categorías)
    Esto puede tardar 10-15 minutos pero solo se hace UNA VEZ
    """
    print("="*80)
    print("🚀 PRECARGA COMPLETA DEL CATÁLOGO DE LA GALLEGA")
    print("="*80)
    print()
    print("⚠️  Este proceso puede tardar 10-15 minutos")
    print("⚠️  Descargará TODOS los productos de TODAS las categorías")
    print("⚠️  Solo se hace UNA VEZ, luego las búsquedas serán instantáneas")
    print()
    input("Presiona ENTER para continuar...")
    print()
    
    scraper = ScraperLaGallega()
    
    # Obtener TODAS las categorías (136 total)
    todas_las_categorias = scraper.categorias
    print(f"📊 Total de categorías a procesar: {len(todas_las_categorias)}")
    print()
    
    total_productos = 0
    categorias_procesadas = 0
    errores = 0
    
    for i, categoria in enumerate(todas_las_categorias, 1):
        try:
            print(f"[{i}/{len(todas_las_categorias)}] Procesando categoría {categoria}...", end=" ")
            
            url = f"{scraper.base_url}/productosnl.asp?nl={categoria}"
            soup = scraper.hacer_request(url)
            
            if not soup:
                print("❌ Error al cargar")
                errores += 1
                continue
            
            # Buscar todos los productos en esta categoría
            productos_li = soup.find_all('li', class_='cuadProd')
            
            if not productos_li:
                print("⚠️  Sin productos")
                continue
            
            productos_guardados = 0
            
            for prod_li in productos_li:
                try:
                    # Extraer nombre
                    nombre_elem = prod_li.find('div', class_='desc')
                    
                    if not nombre_elem:
                        # Fallback: buscar en alt de imagen
                        img_fallback = prod_li.find('img')
                        if img_fallback and img_fallback.get('alt'):
                            alt = img_fallback.get('alt', '')
                            if ' - ' in alt:
                                nombre = alt.split(' - ', 1)[1]
                            else:
                                nombre = alt
                        else:
                            continue
                    else:
                        nombre = nombre_elem.get_text(strip=True)
                    
                    if not nombre:
                        continue
                    
                    # Extraer precio
                    import re
                    precio_match = re.search(r'\$\s*([\d.,]+)', prod_li.get_text())
                    if not precio_match:
                        continue
                    
                    try:
                        precio = scraper.limpiar_precio(precio_match.group(0))
                    except:
                        continue
                    
                    # Extraer imagen URL
                    img_elem = prod_li.find('img')
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
                    
                    # Extraer URL del producto
                    link = prod_li.find('a', href=True)
                    producto_url = scraper.base_url
                    if link:
                        href = link.get('href', '')
                        if href.startswith('http'):
                            producto_url = href
                        elif href.startswith('/'):
                            producto_url = f"{scraper.base_url}{href}"
                        else:
                            producto_url = f"{scraper.base_url}/{href}"
                    
                    # Verificar si ya existe (para contar duplicados)
                    if nombre in cache_manager.cache['productos']['lagallega']:
                        # Producto duplicado, no contar
                        continue
                    
                    # Guardar en caché (SOLO URLs, no descargar imágenes)
                    cache_manager.agregar_producto(
                        supermercado='lagallega',
                        nombre=nombre,
                        categoria=categoria,
                        precio=precio,
                        url=producto_url,
                        imagen_url=imagen_url
                    )
                    
                    productos_guardados += 1
                    total_productos += 1
                    
                except Exception as e:
                    continue
            
            print(f"✅ {productos_guardados} productos guardados")
            categorias_procesadas += 1
            
            # Guardar caché cada 10 categorías
            if i % 10 == 0:
                cache_manager.guardar_cache()
                print(f"   💾 Caché guardado ({total_productos} productos totales)")
            
            # Pequeña pausa para no saturar el servidor
            sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            errores += 1
            continue
    
    # Guardar caché final
    cache_manager.guardar_cache()
    
    print()
    print("="*80)
    print("✅ PRECARGA COMPLETA FINALIZADA")
    print("="*80)
    print(f"📊 Categorías procesadas: {categorias_procesadas}/{len(todas_las_categorias)}")
    print(f"📦 Total de productos guardados: {total_productos}")
    print(f"❌ Errores: {errores}")
    print()
    print(f"💾 Caché guardado en: {cache_manager.cache_file}")
    print()
    print("🚀 Ahora las búsquedas en La Gallega serán INSTANTÁNEAS!")
    print()

if __name__ == "__main__":
    precargar_catalogo_completo()
