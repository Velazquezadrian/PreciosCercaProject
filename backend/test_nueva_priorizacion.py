#!/usr/bin/env python3
"""
Test del nuevo sistema de priorización de búsqueda

LÓGICA ESPERADA:
- Query "pan rayado" debe mostrar:
  1. Productos con "pan" Y "rayado" (ordenados alfabéticamente)
  2. Productos con solo "pan" o solo "rayado" (ordenados alfabéticamente)

- Query "dulce de leche" debe mostrar:
  1. Productos con "dulce" Y "de" Y "leche" (alfabético)
  2. Productos con 2 de las 3 palabras (alfabético)
  3. Productos con 1 de las 3 palabras (alfabético)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.services import buscar_productos_similares

# Productos de ejemplo para testing
productos_test_pan = [
    {'nombre': 'Pan Lactal Bimbo 500g', 'precio': 1200, 'supermercado': 'Carrefour'},
    {'nombre': 'Pan Rayado Carrefour 200g', 'precio': 800, 'supermercado': 'Carrefour'},
    {'nombre': 'Pan Rallado Don Satur 250g', 'precio': 950, 'supermercado': 'Día %'},
    {'nombre': 'Pan Francés', 'precio': 500, 'supermercado': 'La Reina'},
    {'nombre': 'Aceite de girasol', 'precio': 2000, 'supermercado': 'Carrefour'},
    {'nombre': 'Pan integral Fargo 350g', 'precio': 1100, 'supermercado': 'Día %'},
    {'nombre': 'Rallado sabor queso 100g', 'precio': 700, 'supermercado': 'La Gallega'},
]

productos_test_dulce = [
    {'nombre': 'Dulce de leche Sancor 400g', 'precio': 2500, 'supermercado': 'Carrefour'},
    {'nombre': 'Alfajor de chocolate', 'precio': 800, 'supermercado': 'Día %'},
    {'nombre': 'Dulce de Batata La Campagnola 500g', 'precio': 1800, 'supermercado': 'La Reina'},
    {'nombre': 'Leche entera La Serenísima 1L', 'precio': 1200, 'supermercado': 'Carrefour'},
    {'nombre': 'Postre de Dulce de Leche Tregar 180g', 'precio': 900, 'supermercado': 'Día %'},
    {'nombre': 'Dulce De Leche Colonial 1kg', 'precio': 4500, 'supermercado': 'La Gallega'},
    {'nombre': 'Chocolate con leche Milka 100g', 'precio': 1500, 'supermercado': 'Carrefour'},
]


def test_busqueda(query: str, productos: list):
    """Prueba una búsqueda y muestra resultados"""
    print("\n" + "="*80)
    print(f"🔍 TEST: Búsqueda '{query}'")
    print("="*80)
    
    resultados = buscar_productos_similares(query, productos)
    
    print(f"\n📊 RESULTADOS ({len(resultados)} productos):")
    print("-" * 80)
    
    if not resultados:
        print("⚠️ No se encontraron productos")
        return
    
    # Agrupar por número de coincidencias
    grupos = {}
    query_palabras = len(query.split())
    
    for prod in resultados:
        coincidencias = prod.get('coincidencias', 0)
        if coincidencias not in grupos:
            grupos[coincidencias] = []
        grupos[coincidencias].append(prod)
    
    # Mostrar grupos ordenados
    for num_coincidencias in sorted(grupos.keys(), reverse=True):
        productos_grupo = grupos[num_coincidencias]
        print(f"\n🏆 GRUPO: {num_coincidencias}/{query_palabras} palabras coinciden ({len(productos_grupo)} productos)")
        print(f"   Orden: Alfabético")
        print("-" * 80)
        
        for i, prod in enumerate(productos_grupo, 1):
            print(f"   {i}. {prod['nombre']:50} ${prod['precio']:6.2f} - {prod['supermercado']}")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║          TEST SISTEMA DE PRIORIZACIÓN Y ORDENAMIENTO                      ║")
    print("║                                                                            ║")
    print("║  Lógica:                                                                   ║")
    print("║  1. Priorizar productos con MÁS palabras coincidentes                    ║")
    print("║  2. Dentro de cada grupo: ORDEN ALFABÉTICO                                ║")
    print("║  3. NO ordenar por precio                                                  ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Test 1: Pan rayado
    test_busqueda("pan rayado", productos_test_pan)
    
    # Test 2: Dulce de leche
    test_busqueda("dulce de leche", productos_test_dulce)
    
    # Test 3: Solo "pan"
    test_busqueda("pan", productos_test_pan)
    
    print("\n\n")
    print("="*80)
    print("✅ TESTS COMPLETADOS")
    print("="*80)
    print("\nObservaciones:")
    print("- Los productos con TODAS las palabras deben aparecer primero")
    print("- Dentro de cada grupo, orden alfabético (ignora mayúsculas/minúsculas)")
    print("- El precio NO afecta el orden")
    print("\n")
