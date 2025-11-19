#!/usr/bin/env python3
"""Test específico con los productos problemáticos de la app"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.services import buscar_productos_similares

# Productos que aparecen en la captura de pantalla
productos = [
    {'nombre': 'Alimento en pan para untar Manty 200 g.', 'precio': 2629, 'supermercado': 'Carrefour'},
    {'nombre': 'Aperitivo con alcohol Carpano Punt E Mes 750 cc.', 'precio': 9399, 'supermercado': 'Carrefour'},
    {'nombre': 'Camara de Seguridad Panacom IP5962 con Panel Solar', 'precio': 139999, 'supermercado': 'Carrefour'},
    {'nombre': 'Campana Extractor LG 60 cm Plata HCEZ2415S2', 'precio': 821589, 'supermercado': 'Carrefour'},
    {'nombre': 'Cuchilla Carrefour para pan mango madera', 'precio': 6990, 'supermercado': 'Carrefour'},
    {'nombre': 'Cuchillo Tefal de pan 20 cm ice force (k2320414)', 'precio': 26459, 'supermercado': 'Carrefour'},
]

print("="*70)
print("🧪 TEST: Productos de la captura de pantalla - búsqueda 'pan'")
print("="*70)

query = "pan"
filtrados = buscar_productos_similares(query, productos)

print(f"\n📊 Total productos originales: {len(productos)}")
print(f"📊 Total productos filtrados: {len(filtrados)}")

print("\n✅ PRODUCTOS QUE DEBERÍAN APARECER:")
print("   1. Alimento en pan para untar")
print("   2. Cuchilla para pan")
print("   3. Cuchillo de pan")

print("\n❌ PRODUCTOS QUE NO DEBERÍAN APARECER:")
print("   1. Aperitivo Carpano (tiene 'pan' dentro de 'Carpano')")
print("   2. Camara Panacom (tiene 'pan' dentro de 'Panacom')")
print("   3. Campana Extractor (tiene 'pan' dentro de 'Campana')")

print("\n" + "="*70)
print("RESULTADOS FILTRADOS:")
print("="*70)

for i, p in enumerate(filtrados, 1):
    print(f"{i}. {p['nombre']}")

print("\n" + "="*70)
print("VERIFICACIONES:")
print("="*70)

nombres_filtrados = [p['nombre'].lower() for p in filtrados]

# Debe incluir
assert any('alimento en pan' in n for n in nombres_filtrados), "❌ Debe incluir 'Alimento en pan'"
print("✅ Incluye 'Alimento en pan para untar'")

assert any('cuchilla' in n and 'para pan' in n for n in nombres_filtrados), "❌ Debe incluir 'Cuchilla para pan'"
print("✅ Incluye 'Cuchilla para pan'")

assert any('cuchillo' in n and 'de pan' in n for n in nombres_filtrados), "❌ Debe incluir 'Cuchillo de pan'"
print("✅ Incluye 'Cuchillo de pan'")

# NO debe incluir
assert not any('carpano' in n for n in nombres_filtrados), "❌ NO debe incluir 'Carpano'"
print("✅ NO incluye 'Carpano' (correcto)")

assert not any('panacom' in n for n in nombres_filtrados), "❌ NO debe incluir 'Panacom'"
print("✅ NO incluye 'Panacom' (correcto)")

assert not any('campana' in n for n in nombres_filtrados), "❌ NO debe incluir 'Campana'"
print("✅ NO incluye 'Campana' (correcto)")

print("\n" + "="*70)
print("✅ TEST EXITOSO: Filtro funciona correctamente")
print("="*70)
