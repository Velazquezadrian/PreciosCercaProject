#!/usr/bin/env python3
from backend.productos.scrapers.scraper_coto import ScraperCoto

scraper = ScraperCoto()

# Probar con 3 páginas (216 productos)
print("\n🧪 PRUEBA DE PAGINACIÓN - 3 PÁGINAS")
print("="*80)

productos = scraper.buscar_productos('leche', max_paginas=3)

print(f"\n✅ Total productos obtenidos: {len(productos)}")
print(f"\nPRIMEROS 10 PRODUCTOS:")
for i, p in enumerate(productos[:10], 1):
    print(f"  {i}. {p['nombre'][:50]} - ${p['precio']}")
