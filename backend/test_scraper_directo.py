#!/usr/bin/env python3
"""
Prueba directa del scraper de La Gallega
"""

from productos.scrapers.scraper_lagallega import ScraperLaGallega

print("🔍 Probando ScraperLaGallega directamente...\n")

scraper = ScraperLaGallega()

# Prueba 1: Una palabra
print("=" * 60)
print("Búsqueda: 'dulce'")
productos = scraper.buscar_productos('dulce')
print(f"✅ Encontrados: {len(productos)} productos")
if productos:
    for i, p in enumerate(productos[:3], 1):
        print(f"  {i}. {p['nombre']} - ${p['precio']}")

# Prueba 2: Palabras compuestas
print("\n" + "=" * 60)
print("Búsqueda: 'dulce de leche'")
productos = scraper.buscar_productos('dulce de leche')
print(f"✅ Encontrados: {len(productos)} productos")
if productos:
    for i, p in enumerate(productos[:3], 1):
        print(f"  {i}. {p['nombre']} - ${p['precio']}")
else:
    print("⚠️  No se encontraron productos")

print("\n" + "=" * 60)
