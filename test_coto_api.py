#!/usr/bin/env python3
"""
Investigar API interna de Coto
"""
import requests
import json

# Probar diferentes endpoints posibles
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.cotodigital.com.ar/'
})

endpoints_posibles = [
    'https://www.cotodigital.com.ar/api/products?search=leche',
    'https://www.cotodigital.com.ar/api/productos?q=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/api/productos?q=leche',
    'https://www.cotodigital.com.ar/cdigi/api/products?search=leche',
    'https://api.cotodigital.com.ar/products?search=leche',
]

print("=== PROBANDO ENDPOINTS ===\n")
for endpoint in endpoints_posibles:
    try:
        print(f"Probando: {endpoint}")
        r = session.get(endpoint, timeout=5)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            print(f"  Content-Type: {r.headers.get('content-type')}")
            print(f"  Tamaño: {len(r.text)} bytes")
            if 'json' in r.headers.get('content-type', ''):
                data = r.json()
                print(f"  JSON keys: {list(data.keys())}")
        print()
    except Exception as e:
        print(f"  Error: {e}\n")

# Intentar con el endpoint de búsqueda actual pero con headers correctos
print("\n=== PROBANDO BROWSE CON JSON HEADER ===\n")
try:
    r = session.get('https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20', timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('content-type')}")
    
    # Ver si hay algo en las cookies o localStorage
    print(f"Cookies: {r.cookies.get_dict()}")
    
except Exception as e:
    print(f"Error: {e}")
