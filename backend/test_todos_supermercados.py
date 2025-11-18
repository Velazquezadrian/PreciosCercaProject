#!/usr/bin/env python3
"""
Test comparativo: ¿Cuántos productos encuentra cada scraper?
=============================================================

Compara resultados de búsquedas comunes en los 4 supermercados
para detectar si hay productos faltantes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.scrapers.scraper_carrefour import ScraperCarrefour
from productos.scrapers.scraper_dia import ScraperDia
from productos.scrapers.scraper_lareina import ScraperLaReina
from productos.scrapers.scraper_lagallega import ScraperLaGallega

print("🔍 TEST COMPARATIVO DE SCRAPERS")
print("=" * 70)

# Inicializar scrapers
scrapers = {
    'Carrefour': ScraperCarrefour(),
    'Día %': ScraperDia(),
    'La Reina': ScraperLaReina(),
    'La Gallega': ScraperLaGallega()
}

# Búsquedas de prueba
queries = ['leche', 'arroz', 'aceite', 'pan', 'azucar']

for query in queries:
    print(f"\n📊 Búsqueda: '{query}'")
    print("-" * 70)
    
    for nombre, scraper in scrapers.items():
        try:
            productos = scraper.buscar_productos(query)
            print(f"  {nombre:15} → {len(productos):3} productos")
        except Exception as e:
            print(f"  {nombre:15} → ❌ ERROR: {e}")

print("\n" + "=" * 70)
print("💡 ANÁLISIS:")
print("Si un supermercado muestra consistentemente MENOS productos que")
print("los demás, probablemente tiene categorías/endpoints faltantes.")
print("=" * 70)
