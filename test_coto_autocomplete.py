#!/usr/bin/env python3
"""
Investigar endpoint de autocompletado de Coto (con descompresión)
"""
import requests
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',  # Acepta compresión
    'Referer': 'https://www.cotodigital.com.ar/',
})

print("🔍 PROBANDO AUTOCOMPLETADO DE COTO")
print("="*80)
print()

# Cargar página principal primero
session.get('https://www.cotodigital.com.ar/', timeout=10)

urls_a_probar = [
    'https://www.cotodigital.com.ar/sitios/cdigi/api/autocomplete?term=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/api/productos/search?q=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/api/productos/buscar?q=leche',
]

for url in urls_a_probar:
    print(f"Probando: {url}")
    try:
        # requests automáticamente descomprime gzip
        r = session.get(url, timeout=10)
        
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('content-type')}")
        print(f"Content-Encoding: {r.headers.get('content-encoding')}")
        
        if r.status_code == 200:
            # Ver si es JSON
            try:
                data = r.json()
                print(f"✅ JSON VÁLIDO!")
                print(f"Tipo: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"Total items: {len(data)}")
                    if len(data) > 0:
                        print(f"Primer item: {data[0]}")
                
                print(f"\nRESPUESTA COMPLETA:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
                
            except Exception as e:
                print(f"❌ No es JSON: {e}")
                print(f"Primeros 500 chars:")
                print(r.text[:500])
        
        print()
        print("-"*80)
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()

print()
print("="*80)
print("🔍 PROBANDO ENDPOINT DE BROWSE CON AJAX")
print("="*80)
print()

# Algunas SPAs tienen endpoints _ajax o _data
browse_urls = [
    'https://www.cotodigital.com.ar/sitios/cdigi/browse/_ajax?_Ntt=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/browse.json?_Ntt=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/browse/_data?_Ntt=leche',
]

for url in browse_urls:
    print(f"Probando: {url}")
    try:
        r = session.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"✅ JSON encontrado!")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
            except:
                print(f"Texto: {r.text[:200]}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
