#!/usr/bin/env python3
"""
Probar scraper de La Gallega con Selenium mejorado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.scrapers.scraper_lagallega_selenium import ScraperLaGallegaSelenium

print("🚀 Probando ScraperLaGallegaSelenium (mejorado con undetected-chromedriver)\n")

scraper = ScraperLaGallegaSelenium()

# Prueba 1
print("=" * 60)
print("Búsqueda: 'leche'")
productos = scraper.buscar_productos('leche')
print(f"\n📊 Total encontrados: {len(productos)} productos\n")
if productos:
    print("🏆 Primeros 5 resultados:")
    for i, p in enumerate(productos[:5], 1):
        print(f"  {i}. {p['nombre']}")
        print(f"     💰 ${p['precio']:.2f}")
        if p.get('imagen'):
            print(f"     📷 {p['imagen'][:50]}...")
else:
    print("⚠️  No se encontraron productos")

# Prueba 2
print("\n" + "=" * 60)
print("Búsqueda: 'dulce de leche'")
productos = scraper.buscar_productos('dulce de leche')
print(f"\n📊 Total encontrados: {len(productos)} productos\n")
if productos:
    print("🏆 Primeros 5 resultados:")
    for i, p in enumerate(productos[:5], 1):
        print(f"  {i}. {p['nombre']}")
        print(f"     💰 ${p['precio']:.2f}")
        if p.get('imagen'):
            print(f"     📷 {p['imagen'][:50]}...")
else:
    print("⚠️  No se encontraron productos")

print("\n" + "=" * 60)
print("✅ Prueba completada")
print("Cerrando navegador...")
scraper._close_driver()
print("✅ Navegador cerrado")
