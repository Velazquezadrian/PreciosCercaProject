#!/usr/bin/env python3
"""
Script para precargar SOLO Carrefour
Descarga el catálogo completo (~90,000 productos)
Tiempo estimado: 15-20 minutos
"""

import sys
import os
from datetime import datetime

# Agregar path del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from productos.scrapers.scraper_carrefour import ScraperCarrefour
from cache_manager import cache_manager

def main():
    print("")
    print("╔" + "="*78 + "╗")
    print("║" + " PRECARGA COMPLETA DE CARREFOUR ".center(78) + "║")
    print("╚" + "="*78 + "╝")
    print("")
    print(f"🕐 Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📦 Catálogo estimado: ~90,000 productos")
    print(f"⏱️  Duración estimada: 15-20 minutos")
    print("")
    
    try:
        # Inicializar scraper
        scraper = ScraperCarrefour()
        
        # Ejecutar precarga completa
        scraper._auto_precargar()
        
        # Resumen final
        total_carrefour = len(cache_manager.cache['productos'].get('carrefour', {}))
        print("")
        print("╔" + "="*78 + "╗")
        print("║" + " RESUMEN FINAL ".center(78) + "║")
        print("╚" + "="*78 + "╝")
        print("")
        print(f"✅ Carrefour: {total_carrefour:,} productos")
        print(f"🕐 Fin: {datetime.now().strftime('%H:%M:%S')}")
        print("")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Precarga interrumpida por el usuario (Ctrl+C)")
        print("💾 Los productos descargados hasta ahora están guardados en el caché")
        total_carrefour = len(cache_manager.cache['productos'].get('carrefour', {}))
        print(f"📊 Total actual: {total_carrefour:,} productos")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
