#!/usr/bin/env python3
"""
Script para probar búsquedas con palabras compuestas
"""

import requests
import json

def probar_busqueda(query):
    print(f"\n{'='*60}")
    print(f"🔍 Probando búsqueda: '{query}'")
    print('='*60)
    
    try:
        response = requests.get('http://localhost:8000/products', params={'query': query}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_encontrados', 0)
            resultados = data.get('resultados', [])
            
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Productos encontrados: {total}")
            
            if resultados:
                print(f"\n🏆 Primeros 5 resultados:")
                for i, prod in enumerate(resultados[:5], 1):
                    print(f"  {i}. {prod['nombre']}")
                    print(f"     💰 ${prod['precio']:.2f} - {prod['supermercado']}")
            else:
                print("⚠️  No se encontraron productos")
        else:
            print(f"❌ Error: Status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está corriendo en http://localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║  PRUEBA DE BÚSQUEDAS CON PALABRAS COMPUESTAS              ║
║  PreciosCerca Server                                       ║
╚════════════════════════════════════════════════════════════╝
""")
    
    # Pruebas con diferentes términos
    terminos_prueba = [
        "dulce de leche",
        "aceite de oliva",
        "papel higiénico",
        "agua mineral",
        "leche",
        "pan"
    ]
    
    for termino in terminos_prueba:
        probar_busqueda(termino)
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas")
    print("="*60)
