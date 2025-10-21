import requests
import json

print("=== PRUEBA BLOQUE 3 - API CONSOLIDADA ===")
print()

try:
    # Probar endpoint con múltiples scrapers
    response = requests.get('http://127.0.0.1:8000/products?query=arroz', timeout=30)
    
    print(f"Status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Query: '{data['query']}'")
        print(f"Total encontrados: {data['total_encontrados']}")
        
        if data['total_encontrados'] > 0:
            # Agrupar por supermercado
            supermercados = {}
            for producto in data['resultados']:
                super_nombre = producto['supermercado']
                if super_nombre not in supermercados:
                    supermercados[super_nombre] = []
                supermercados[super_nombre].append(producto)
            
            print(f"\nSupermercados integrados: {len(supermercados)}")
            for supermercado, productos in supermercados.items():
                print(f"  - {supermercado}: {len(productos)} productos")
                # Mostrar primer producto de ejemplo
                if productos:
                    ejemplo = productos[0]
                    print(f"    Ejemplo: {ejemplo['nombre']} - ${ejemplo['precio']}")
            
            print(f"\nBLOQUE 3 EXITOSO: API consolidada funcionando!")
            
        else:
            print("No se encontraron productos con 'arroz'")
            print("Esto puede ser normal - probando con otro termino...")
            
            # Probar con "cafe"
            response2 = requests.get('http://127.0.0.1:8000/products?query=cafe', timeout=20)
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"Cafe encontrados: {data2['total_encontrados']}")
            
    else:
        print(f"ERROR HTTP: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== FIN PRUEBA ===")