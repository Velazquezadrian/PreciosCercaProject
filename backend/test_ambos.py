#!/usr/bin/env python3
"""Test del servidor completo con ambos supermercados"""

import sys
sys.path.append('.')

from productos.scrapers.scraper_carrefour import ScraperCarrefour
from productos.scrapers.scraper_dia import ScraperDia

query = "leche"

print("="*60)
print(f"🔍 Buscando: '{query}'")
print("="*60)

# Carrefour
print("\n📦 CARREFOUR:")
scraper_carrefour = ScraperCarrefour()
productos_carrefour = scraper_carrefour.buscar_productos(query)
print(f"   ✅ {len(productos_carrefour)} productos encontrados")
if productos_carrefour:
    print(f"   💰 Más barato: {productos_carrefour[0]['nombre']} - ${productos_carrefour[0]['precio']:.2f}")

# Día
print("\n📦 DÍA %:")
scraper_dia = ScraperDia()
productos_dia = scraper_dia.buscar_productos(query)
print(f"   ✅ {len(productos_dia)} productos encontrados")
if productos_dia:
    # Ordenar por precio
    productos_dia_sorted = sorted(productos_dia, key=lambda x: x['precio'])
    print(f"   💰 Más barato: {productos_dia_sorted[0]['nombre']} - ${productos_dia_sorted[0]['precio']:.2f}")

# Combinados
print("\n" + "="*60)
todos = productos_carrefour + productos_dia
todos.sort(key=lambda x: x['precio'])

print(f"📊 TOTAL: {len(todos)} productos en {2} supermercados")
print("\n🏆 TOP 5 MÁS BARATOS:")
for i, p in enumerate(todos[:5], 1):
    print(f"   {i}. {p['nombre']}")
    print(f"      💰 ${p['precio']:.2f} - {p['supermercado']}")
print("="*60)
