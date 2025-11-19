#!/usr/bin/env python3
"""
Test comparativo: Scrapers ANTES vs DESPUÉS de optimización con categorías

ANTES:
- Carrefour: Búsqueda directa con ft= (50 productos máx)
- Día: Búsqueda directa con ft= (50 productos máx)

DESPUÉS:
- Carrefour: 148 categorías
- Día: 122 categorías
- La Reina: 212 categorías (ya optimizado)
- La Gallega: 136 categorías (ya optimizado)

Total: 618 categorías en 4 supermercados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.scrapers.scraper_carrefour import ScraperCarrefour
from productos.scrapers.scraper_dia import ScraperDia
from productos.scrapers.scraper_lareina import ScraperLaReina
from productos.scrapers.scraper_lagallega import ScraperLaGallega

def probar_scraper(scraper, nombre, query):
    """Prueba un scraper y muestra estadísticas"""
    print(f"\n{'='*80}")
    print(f"🛒 {nombre} - Búsqueda: '{query}'")
    print(f"{'='*80}")
    
    productos = scraper.buscar_productos(query)
    
    print(f"\n📊 Resultados:")
    print(f"   Total productos: {len(productos)}")
    
    if productos:
        # Mostrar primeros 5
        print(f"\n   Primeros 5 productos:")
        for i, p in enumerate(productos[:5], 1):
            print(f"      {i}. {p['nombre'][:60]} - ${p['precio']:.2f}")
        
        # Estadísticas de precios
        precios = [p['precio'] for p in productos]
        print(f"\n   💰 Precios:")
        print(f"      Mínimo: ${min(precios):.2f}")
        print(f"      Máximo: ${max(precios):.2f}")
        print(f"      Promedio: ${sum(precios)/len(precios):.2f}")
    else:
        print("   ⚠️ No se encontraron productos")
    
    return productos


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║         TEST COMPARATIVO - SCRAPERS CON CATEGORÍAS OPTIMIZADAS            ║")
    print("║                                                                            ║")
    print("║  Carrefour: 148 categorías  |  Día: 122 categorías                       ║")
    print("║  La Reina:  212 categorías  |  La Gallega: 136 categorías                ║")
    print("║                                                                            ║")
    print("║  TOTAL: 618 categorías mapeadas                                           ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Inicializar scrapers
    scrapers = {
        'Carrefour': ScraperCarrefour(),
        'Día %': ScraperDia(),
        'La Reina': ScraperLaReina(),
        'La Gallega': ScraperLaGallega()
    }
    
    # Búsquedas de prueba
    queries = ['leche', 'dulce de leche', 'aceite', 'pan']
    
    for query in queries:
        print(f"\n\n{'#'*80}")
        print(f"# BÚSQUEDA: '{query}'")
        print(f"{'#'*80}")
        
        resultados = {}
        
        for nombre, scraper in scrapers.items():
            productos = probar_scraper(scraper, nombre, query)
            resultados[nombre] = len(productos)
        
        # Resumen comparativo
        print(f"\n{'='*80}")
        print(f"📊 RESUMEN COMPARATIVO - '{query}'")
        print(f"{'='*80}")
        for nombre, count in resultados.items():
            print(f"   {nombre:15} {count:3} productos")
        print(f"   {'TOTAL':15} {sum(resultados.values()):3} productos")
    
    print("\n\n")
    print("=" * 80)
    print("✅ TEST COMPLETADO")
    print("=" * 80)
    print("\n💡 Compará estos resultados con test_todos_supermercados.py (versión anterior)")
    print("\n")
