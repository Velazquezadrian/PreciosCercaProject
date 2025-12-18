#!/usr/bin/env python3
from backend.productos.scrapers.scraper_coto import ScraperCoto

scraper = ScraperCoto()
productos = scraper.buscar_productos('leche')

print(f'\n✅ Encontrados: {len(productos)} productos\n')
print("PRIMEROS 5 PRODUCTOS:")
for i, p in enumerate(productos[:5]):
    print(f"  {i+1}. {p['nombre']}")
    print(f"      Precio: ${p['precio']}")
    print(f"      Imagen: {p.get('imagen', 'N/A')[:60]}...")
    print()
