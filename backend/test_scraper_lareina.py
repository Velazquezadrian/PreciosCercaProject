#!/usr/bin/env python3
"""
Test scraper La Reina actualizado con 212 categorías
"""
from productos.scrapers.scraper_lareina import ScraperLaReina

print("=" * 60)
print("TEST SCRAPER LA REINA - 212 CATEGORÍAS")
print("=" * 60)

scraper = ScraperLaReina()
print(f"Categorías disponibles: {len(scraper.categorias)}")

# Test 1: leche (antes solo 7)
print("\n🔍 Buscando 'leche'...")
productos = scraper.buscar_productos('leche')
print(f"✅ Encontrados: {len(productos)} productos")
for i, p in enumerate(productos[:10], 1):
    print(f"  {i}. {p['nombre'][:60]} - ${p['precio']}")

# Test 2: arroz (antes solo 3)
print("\n🔍 Buscando 'arroz'...")
productos = scraper.buscar_productos('arroz')
print(f"✅ Encontrados: {len(productos)} productos")
for i, p in enumerate(productos[:10], 1):
    print(f"  {i}. {p['nombre'][:60]} - ${p['precio']}")

# Test 3: azucar (antes solo 1)
print("\n🔍 Buscando 'azucar'...")
productos = scraper.buscar_productos('azucar')
print(f"✅ Encontrados: {len(productos)} productos")
for i, p in enumerate(productos[:10], 1):
    print(f"  {i}. {p['nombre'][:60]} - ${p['precio']}")

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
