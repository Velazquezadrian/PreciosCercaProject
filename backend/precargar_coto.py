#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de precarga masiva de Coto Digital
Descarga el catálogo completo navegando por páginas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from productos.scrapers.scraper_coto import ScraperCoto
from cache_manager import cache_manager
from time import sleep
from datetime import datetime

def precargar_coto_completo(max_paginas=50):
    """
    Descarga el catálogo completo de Coto Digital
    
    Args:
        max_paginas: Número máximo de páginas a descargar (cada página = 72 productos)
                     50 páginas = ~3,600 productos
                     100 páginas = ~7,200 productos
                     395 páginas = ~28,433 productos (COMPLETO)
    """
    print("")
    print("="*80)
    print("🚀 PRECARGA MASIVA: COTO DIGITAL")
    print("="*80)
    print(f"📅 Inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📊 Páginas a descargar: {max_paginas}")
    print(f"📦 Productos estimados: ~{max_paginas * 72:,}")
    print("="*80)
    print("")
    
    scraper = ScraperCoto()
    scraper._precargando = True  # Desactivar autoprecarga
    
    total_agregados = 0
    paginas_exitosas = 0
    productos_unicos = set()
    
    try:
        for pagina in range(max_paginas):
            offset = pagina * 72
            print(f"📄 Página {pagina + 1}/{max_paginas} (productos {offset + 1}-{offset + 72})...", end=" ", flush=True)
            
            try:
                # Obtener página del catálogo completo (sin búsqueda)
                productos = scraper._obtener_pagina(query=None, offset=offset, limit=72)
                
                if not productos or len(productos) == 0:
                    print("⚠️  Sin más productos, finalizando.")
                    break
                
                # Contar productos únicos
                productos_nuevos = 0
                for prod in productos:
                    nombre_key = prod['nombre'].lower()
                    if nombre_key not in productos_unicos:
                        productos_unicos.add(nombre_key)
                        productos_nuevos += 1
                        
                        # Guardar en caché
                        cache_manager.agregar_producto(
                            supermercado='coto',
                            nombre=prod['nombre'],
                            categoria='',
                            precio=prod['precio'],
                            url=prod['url'],
                            imagen_url=prod['imagen']
                        )
                
                total_agregados += productos_nuevos
                paginas_exitosas += 1
                
                print(f"✅ {len(productos)} productos (+{productos_nuevos} nuevos)")
                
                # Guardar caché cada 10 páginas
                if (pagina + 1) % 10 == 0:
                    cache_manager.guardar_cache()
                    print(f"   💾 Caché guardado - Total acumulado: {total_agregados:,} productos únicos")
                
                # Pausa para no sobrecargar el servidor
                if (pagina + 1) % 5 == 0:
                    sleep(2)
                else:
                    sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Precarga interrumpida (Ctrl+C)")
    
    finally:
        # Guardar caché final
        cache_manager.guardar_cache()
        
        print("")
        print("="*80)
        print("📊 RESUMEN FINAL")
        print("="*80)
        print(f"✅ Páginas procesadas: {paginas_exitosas}/{max_paginas}")
        print(f"✅ Productos únicos agregados: {total_agregados:,}")
        print(f"✅ Total en caché de Coto: {len(cache_manager.cache['productos'].get('coto', {})):,}")
        print(f"⏱️  Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*80)
        print("")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Precarga masiva de Coto Digital')
    parser.add_argument('--paginas', type=int, default=50, 
                        help='Número de páginas a descargar (default: 50)')
    parser.add_argument('--completo', action='store_true',
                        help='Descargar catálogo completo (~395 páginas)')
    
    args = parser.parse_args()
    
    max_paginas = 395 if args.completo else args.paginas
    
    print(f"\n⚠️  ADVERTENCIA: Se descargarán ~{max_paginas * 72:,} productos")
    print(f"⏱️  Tiempo estimado: ~{max_paginas * 0.5 / 60:.1f} minutos")
    
    if args.completo:
        respuesta = input("\n¿Descargar catálogo COMPLETO? (s/n): ")
        if respuesta.lower() != 's':
            print("Operación cancelada")
            sys.exit(0)
    
    precargar_coto_completo(max_paginas=max_paginas)
