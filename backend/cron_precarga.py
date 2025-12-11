#!/usr/bin/env python3
"""
Tarea programada: Precarga diaria de productos
==============================================

Ejecuta precarga completa de todos los supermercados a las 8:00 AM
Solo descarga: nombres, precios, URLs de productos (NO imágenes)

Uso:
    python cron_precarga.py

Autor: PreciosCerca Team
Fecha: Diciembre 2025
"""

import sys
import os
from datetime import datetime

# Agregar directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from productos.scrapers.scraper_carrefour import ScraperCarrefour
from productos.scrapers.scraper_dia import ScraperDia
from productos.scrapers.scraper_lareina import ScraperLaReina
from productos.scrapers.scraper_lagallega import ScraperLaGallega
from productos.scrapers.scraper_coto import ScraperCoto
from cache_manager import cache_manager

def ejecutar_precarga_completa():
    """
    Ejecuta precarga de todos los supermercados
    """
    print("=" * 80)
    print(f"🕐 PRECARGA AUTOMÁTICA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80)
    print("📊 Iniciando precarga de todos los supermercados...")
    print("⚠️  Este proceso puede tardar 30-40 minutos")
    print("⚠️  Solo descarga: nombres, precios, URLs (NO imágenes)")
    print("")
    
    # Scrapers a precargar
    scrapers = {
        'Carrefour': ScraperCarrefour(),
        'Día %': ScraperDia(),
        'La Reina': ScraperLaReina(),
        'La Gallega': ScraperLaGallega(),
        'Coto': ScraperCoto()
    }
    
    resultados = {}
    
    for nombre, scraper in scrapers.items():
        try:
            print(f"\n{'='*80}")
            print(f"🛒 {nombre}")
            print(f"{'='*80}")
            
            # Forzar autoprecarga llamando al método privado
            if hasattr(scraper, '_auto_precargar'):
                scraper._auto_precargar()
                
                # Contar productos en caché
                total = len(cache_manager.cache['productos'].get(
                    nombre.lower().replace(' ', '').replace('%', ''), {}
                ))
                resultados[nombre] = total
                print(f"✅ {nombre}: {total} productos en caché")
            else:
                print(f"⚠️ {nombre}: No tiene método de autoprecarga")
                resultados[nombre] = 0
                
        except Exception as e:
            print(f"❌ {nombre}: Error - {e}")
            resultados[nombre] = 0
    
    # Guardar caché final
    cache_manager.guardar_cache()
    
    # Resumen
    print("\n" + "=" * 80)
    print("✅ PRECARGA COMPLETADA")
    print("=" * 80)
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📊 Resultados:")
    total_general = 0
    for nombre, cantidad in resultados.items():
        print(f"   - {nombre}: {cantidad:,} productos")
        total_general += cantidad
    print(f"\n🎯 TOTAL: {total_general:,} productos en caché")
    print("=" * 80)
    print("")
    
    return resultados

if __name__ == "__main__":
    try:
        ejecutar_precarga_completa()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        sys.exit(1)
