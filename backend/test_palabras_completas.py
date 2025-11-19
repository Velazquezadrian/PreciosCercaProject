#!/usr/bin/env python3
"""
Test de búsqueda con palabras completas
========================================
Verifica que "pan" no coincida con "panasonic"
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from productos.services import buscar_productos_similares

def test_palabras_completas():
    """Test que verifica búsqueda de palabras completas"""
    
    # Productos de prueba
    productos = [
        {'nombre': 'Pan francés La Reina 500g', 'precio': 1200, 'supermercado': 'La Reina'},
        {'nombre': 'Pan rallado Don Satur 250g', 'precio': 800, 'supermercado': 'Carrefour'},
        {'nombre': 'Pan lactal Bimbo 500g', 'precio': 1500, 'supermercado': 'Día %'},
        {'nombre': 'Panasonic TV 32 pulgadas', 'precio': 45000, 'supermercado': 'Carrefour'},
        {'nombre': 'Panadol 500mg 20 comprimidos', 'precio': 2500, 'supermercado': 'Día %'},
        {'nombre': 'Pan dulce Valente 400g', 'precio': 3200, 'supermercado': 'La Gallega'},
    ]
    
    print("\n" + "="*70)
    print("🧪 TEST: Búsqueda de palabra completa 'pan'")
    print("="*70)
    
    # Buscar "pan" (palabra completa)
    query = "pan"
    resultados = buscar_productos_similares(query, productos)
    
    print(f"\n🔍 Query: '{query}'")
    print(f"📊 Total encontrados: {len(resultados)}\n")
    
    # Mostrar resultados
    print("✅ RESULTADOS (deberían ser solo productos con 'pan' como palabra completa):")
    for i, p in enumerate(resultados, 1):
        print(f"  {i}. {p['nombre']}")
    
    # Verificar que NO incluye "panasonic" ni "panadol"
    nombres_resultados = [p['nombre'].lower() for p in resultados]
    
    print("\n" + "-"*70)
    print("🧪 VERIFICACIONES:")
    
    # Debe incluir productos con "pan" como palabra completa
    assert any('pan francés' in n for n in nombres_resultados), "❌ Debería incluir 'Pan francés'"
    print("✅ Incluye 'Pan francés'")
    
    assert any('pan rallado' in n for n in nombres_resultados), "❌ Debería incluir 'Pan rallado'"
    print("✅ Incluye 'Pan rallado'")
    
    assert any('pan lactal' in n for n in nombres_resultados), "❌ Debería incluir 'Pan lactal'"
    print("✅ Incluye 'Pan lactal'")
    
    assert any('pan dulce' in n for n in nombres_resultados), "❌ Debería incluir 'Pan dulce'"
    print("✅ Incluye 'Pan dulce'")
    
    # NO debe incluir "panasonic" ni "panadol"
    assert not any('panasonic' in n for n in nombres_resultados), "❌ NO debería incluir 'Panasonic'"
    print("✅ NO incluye 'Panasonic' (correcto)")
    
    assert not any('panadol' in n for n in nombres_resultados), "❌ NO debería incluir 'Panadol'"
    print("✅ NO incluye 'Panadol' (correcto)")
    
    print("\n" + "="*70)
    print("✅ TEST EXITOSO: Búsqueda de palabras completas funciona correctamente")
    print("="*70)


def test_pan_rayado():
    """Test con búsqueda de múltiples palabras"""
    
    productos = [
        {'nombre': 'Pan rallado Don Satur 250g', 'precio': 800, 'supermercado': 'Carrefour'},
        {'nombre': 'Pan rayado Carrefour 200g', 'precio': 650, 'supermercado': 'Carrefour'},
        {'nombre': 'Pan francés La Reina 500g', 'precio': 1200, 'supermercado': 'La Reina'},
        {'nombre': 'Queso rallado Sancor 100g', 'precio': 1500, 'supermercado': 'Día %'},
        {'nombre': 'Panasonic TV 32 pulgadas', 'precio': 45000, 'supermercado': 'Carrefour'},
    ]
    
    print("\n" + "="*70)
    print("🧪 TEST: Búsqueda 'pan rayado' (dos palabras)")
    print("="*70)
    
    query = "pan rayado"
    resultados = buscar_productos_similares(query, productos)
    
    print(f"\n🔍 Query: '{query}'")
    print(f"📊 Total encontrados: {len(resultados)}\n")
    
    print("✅ RESULTADOS:")
    for i, p in enumerate(resultados, 1):
        coincidencias = p.get('coincidencias', 0)
        print(f"  {i}. {p['nombre']} ({coincidencias}/2 palabras)")
    
    # Verificaciones
    nombres_resultados = [p['nombre'].lower() for p in resultados]
    
    print("\n" + "-"*70)
    print("🧪 VERIFICACIONES:")
    
    # Debe priorizar productos con ambas palabras
    primer_resultado = resultados[0]['nombre'].lower()
    assert 'pan' in primer_resultado and ('rayado' in primer_resultado or 'rallado' in primer_resultado), \
        "❌ Primer resultado debería tener 'pan' y 'rayado/rallado'"
    print(f"✅ Primer resultado tiene ambas palabras: {resultados[0]['nombre']}")
    
    # NO debe incluir "Panasonic"
    assert not any('panasonic' in n for n in nombres_resultados), "❌ NO debería incluir 'Panasonic'"
    print("✅ NO incluye 'Panasonic'")
    
    # NO debe incluir "Queso rallado" (no tiene "pan")
    assert not any('queso' in n for n in nombres_resultados), "❌ NO debería incluir 'Queso rallado'"
    print("✅ NO incluye 'Queso rallado' (solo tiene 'rallado', no 'pan')")
    
    print("\n" + "="*70)
    print("✅ TEST EXITOSO: Búsqueda multi-palabra con palabras completas funciona")
    print("="*70)


if __name__ == '__main__':
    try:
        test_palabras_completas()
        test_pan_rayado()
        print("\n🎉 TODOS LOS TESTS PASARON")
    except AssertionError as e:
        print(f"\n❌ TEST FALLÓ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
