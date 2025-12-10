import requests
import json

# Probar paginación local
print("=== PÁGINA 1 (primeros 10) ===")
response = requests.get('http://localhost:8000/products', params={
    'query': 'pan',
    'supermercado': 'lagallega',
    'page': 1,
    'limit': 10
})

data = response.json()
print(f'Total encontrados: {data["total_encontrados"]}')
print(f'Página: {data["page"]}/{data["total_pages"]}')
print(f'Hay más páginas: {data["has_more"]}')
print(f'\nPrimeros 10 productos:')
for p in data["resultados"]:
    print(f' - {p["nombre"]} (${p["precio"]})')

print("\n=== PÁGINA 2 (siguientes 10) ===")
response2 = requests.get('http://localhost:8000/products', params={
    'query': 'pan',
    'supermercado': 'lagallega',
    'page': 2,
    'limit': 10
})

data2 = response2.json()
print(f'Página: {data2["page"]}/{data2["total_pages"]}')
print(f'\nProductos 11-20:')
for p in data2["resultados"]:
    print(f' - {p["nombre"]} (${p["precio"]})')
