#!/usr/bin/env python
# -*- coding: utf-8 -*-

from productos.scrapers.sucursales_data import filtrar_sucursales_por_radio

# Centro de Rosario
lat_rosario = -32.9478
lng_rosario = -60.6394

print("=" * 60)
print("TEST: Sucursales de La Gallega cerca del centro de Rosario")
print("=" * 60)

# Test con radio de 3km
print(f"\n📍 Ubicación test: ({lat_rosario}, {lng_rosario})")
print(f"📏 Radio: 3 km\n")

sucursales = filtrar_sucursales_por_radio(lat_rosario, lng_rosario, 3)

if "La Gallega" in sucursales:
    lista = sucursales["La Gallega"]
    print(f"✅ Encontradas {len(lista)} sucursales de La Gallega dentro de 3km:")
    print()
    
    for suc in lista:
        print(f"  🏪 {suc['nombre']}")
        print(f"      📍 {suc['direccion']}")
        print(f"      📏 Distancia: {suc['distancia_km']:.2f} km")
        print()
else:
    print("❌ No se encontraron sucursales de La Gallega")

# Test con radio de 10km
print("\n" + "=" * 60)
print(f"📏 Radio: 10 km\n")

sucursales_10km = filtrar_sucursales_por_radio(lat_rosario, lng_rosario, 10)

if "La Gallega" in sucursales_10km:
    lista = sucursales_10km["La Gallega"]
    print(f"✅ Total: {len(lista)} sucursales dentro de 10km")
else:
    print("❌ No se encontraron sucursales")
