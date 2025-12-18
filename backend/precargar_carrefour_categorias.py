#!/usr/bin/env python3
"""
Script mejorado para precargar Carrefour usando CATEGORÍAS
Como la API tiene límite en paginación directa, descargamos por categoría
"""

import sys
import os
from datetime import datetime
from time import sleep

# Agregar path del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from cache_manager import cache_manager
import requests

def main():
    print("")
    print("╔" + "="*78 + "╗")
    print("║" + " PRECARGA COMPLETA CARREFOUR (POR CATEGORÍAS) ".center(78) + "║")
    print("╚" + "="*78 + "╝")
    print("")
    print(f"🕐 Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📦 Estrategia: 148 categorías × ~600 productos c/u")
    print(f"⏱️  Duración estimada: 20-25 minutos")
    print("")
    
    # 148 categorías de Carrefour
    categorias = [
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
    
    api_url = "https://www.carrefour.com.ar/api/catalog_system/pub/products/search"
    session = requests.Session()
    productos_unicos = set()
    total_agregados = 0
    
    try:
        print(f"📊 Descargando por categoría (max 100 productos por categoría)...\n")
        
        for idx, cat_id in enumerate(categorias, 1):
            try:
                print(f"[{idx:3d}/148] Categoría {cat_id:3d}...", end=" ", flush=True)
                
                # Request con filtro de categoría
                params = {
                    'fq': f'C:/{cat_id}/',
                    '_from': 0,
                    '_to': 99  # Max 100 productos por categoría
                }
                
                response = session.get(api_url, params=params, timeout=15)
                
                if response.status_code not in [200, 206]:
                    print(f"❌ HTTP {response.status_code}")
                    continue
                
                productos_json = response.json()
                
                if not productos_json:
                    print("⚠️ vacía")
                    continue
                
                # Procesar productos
                nuevos = 0
                for prod in productos_json:
                    try:
                        nombre = prod.get('productName', '').strip()
                        if not nombre or nombre in productos_unicos:
                            continue
                        
                        items = prod.get('items', [])
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
                        
                        # URL
                        producto_url = f"https://www.carrefour.com.ar/{prod.get('linkText', '')}/p"
                        
                        # Guardar en caché
                        cache_manager.agregar_producto(
                            supermercado='carrefour',
                            nombre=nombre,
                            categoria=str(cat_id),
                            precio=float(precio),
                            url=producto_url,
                            imagen_url=imagen_url
                        )
                        
                        productos_unicos.add(nombre)
                        nuevos += 1
                        total_agregados += 1
                        
                    except Exception:
                        continue
                
                print(f"✅ {nuevos:2d} nuevos | Total: {total_agregados:5d}")
                
                # Guardar cada 10 categorías
                if idx % 10 == 0:
                    cache_manager.guardar_cache()
                    print(f"   💾 Caché guardado\n")
                
                # Pausa
                sleep(0.15)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Precarga interrumpida (Ctrl+C)")
    
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cache_manager.guardar_cache()
        total_carrefour = len(cache_manager.cache['productos'].get('carrefour', {}))
        
        print("")
        print("╔" + "="*78 + "╗")
        print("║" + " RESUMEN FINAL ".center(78) + "║")
        print("╚" + "="*78 + "╝")
        print("")
        print(f"✅ Carrefour: {total_carrefour:,} productos")
        print(f"🕐 Fin: {datetime.now().strftime('%H:%M:%S')}")
        print("")

if __name__ == '__main__':
    main()
