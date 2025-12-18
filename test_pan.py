import requests
import json

# Probar Railway con paginación
print("=== PROBANDO RAILWAY ===")
response = requests.get('https://web-production-a6410.up.railway.app/products', params={
    'query': 'pan',
    'supermercado': 'lagallega',
    'page': 1,
    'limit': 30
})

print(f'Status code: {response.status_code}')

if response.status_code == 200:
    data = response.json()
    print(f'Total encontrados: {data.get("total_encontrados", "N/A")}')
    print(f'Página: {data.get("page", "N/A")}/{data.get("total_pages", "N/A")}')
    print(f'Has more: {data.get("has_more", "N/A")}')
    print(f'Resultados en esta página: {len(data.get("resultados", []))}')
    print(f'\nPrimeros 5 productos:')
    for p in data.get("resultados", [])[:5]:
        print(f' - {p["nombre"]} (${p["precio"]})')
else:
    print(f'Error: {response.text[:500]}')
