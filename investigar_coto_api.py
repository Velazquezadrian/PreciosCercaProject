#!/usr/bin/env python3
"""
Investigación profunda de API de Coto Digital
Simula navegador real para encontrar endpoints
"""
import requests
import json
from bs4 import BeautifulSoup

session = requests.Session()

# Headers que simula un navegador real
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.cotodigital.com.ar/',
    'Origin': 'https://www.cotodigital.com.ar',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
})

print("="*80)
print("🔍 INVESTIGACIÓN API COTO DIGITAL")
print("="*80)
print()

# 1. Cargar página principal primero (para obtener cookies)
print("1️⃣ Cargando página principal...")
try:
    r = session.get('https://www.cotodigital.com.ar/', timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Cookies obtenidas: {list(session.cookies.keys())}")
except Exception as e:
    print(f"   Error: {e}")

print()

# 2. Intentar endpoints de búsqueda con diferentes formatos
print("2️⃣ Probando endpoints de búsqueda...")
print()

endpoints_busqueda = [
    # Posibles endpoints REST
    ('https://www.cotodigital.com.ar/api/v1/search?q=leche', 'REST v1'),
    ('https://www.cotodigital.com.ar/api/search?q=leche', 'REST search'),
    ('https://www.cotodigital.com.ar/sitios/cdigi/api/search?term=leche', 'API search'),
    
    # Posibles endpoints con productos
    ('https://www.cotodigital.com.ar/api/products?query=leche', 'Products API'),
    ('https://www.cotodigital.com.ar/api/productos?busqueda=leche', 'Productos API'),
    
    # Posibles endpoints estilo VTEX (como Carrefour)
    ('https://www.cotodigital.com.ar/api/catalog_system/pub/products/search?ft=leche', 'VTEX style'),
    
    # Endpoints internos Angular
    ('https://www.cotodigital.com.ar/sitios/cdigi/producto/buscar?q=leche', 'Angular interno'),
    ('https://www.cotodigital.com.ar/sitios/cdigi/productos?search=leche', 'Angular productos'),
]

for url, nombre in endpoints_busqueda:
    try:
        r = session.get(url, timeout=5)
        print(f"   {nombre}")
        print(f"   URL: {url}")
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            content_type = r.headers.get('content-type', '')
            print(f"   Content-Type: {content_type}")
            print(f"   Tamaño: {len(r.text)} bytes")
            
            if 'json' in content_type:
                try:
                    data = r.json()
                    print(f"   ✅ JSON válido!")
                    print(f"   Keys: {list(data.keys())[:10]}")
                    print(f"   Preview: {str(data)[:200]}...")
                except:
                    print(f"   ❌ No es JSON válido")
            
            # Ver si hay productos en HTML
            if 'html' in content_type:
                soup = BeautifulSoup(r.text, 'html.parser')
                scripts = soup.find_all('script')
                print(f"   Scripts encontrados: {len(scripts)}")
                
                # Buscar datos JSON embebidos en scripts
                for script in scripts:
                    if script.string and 'product' in script.string.lower():
                        print(f"   ⚠️ Script con 'product' encontrado!")
                        print(f"      {script.string[:200]}...")
        
        print()
        
    except Exception as e:
        print(f"   Error: {e}")
        print()

print()
print("3️⃣ Probando GraphQL...")
print()

# Muchas SPAs modernas usan GraphQL
graphql_queries = [
    {
        'url': 'https://www.cotodigital.com.ar/graphql',
        'query': '{"query":"{ products(search: \\"leche\\") { name price } }"}'
    },
    {
        'url': 'https://www.cotodigital.com.ar/api/graphql',
        'query': '{"query":"{ search(term: \\"leche\\") { items { name price } } }"}'
    }
]

for gql in graphql_queries:
    try:
        r = session.post(
            gql['url'],
            json={'query': gql['query']},
            timeout=5
        )
        print(f"   URL: {gql['url']}")
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            print(f"   ✅ Respuesta: {r.text[:200]}...")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()

print()
print("4️⃣ Inspeccionando HTML de búsqueda...")
print()

# Cargar página de búsqueda y buscar datos embebidos
try:
    r = session.get('https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche', timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Buscar scripts con datos JSON
    scripts = soup.find_all('script')
    print(f"   Total scripts: {len(scripts)}")
    
    for idx, script in enumerate(scripts):
        if script.string:
            # Buscar patrones comunes de datos JSON embebidos
            if any(pattern in script.string for pattern in ['window.__INITIAL_STATE__', 'window.__DATA__', '__NEXT_DATA__', 'productData', 'searchResults']):
                print(f"\n   ⚠️ Script #{idx} con datos embebidos:")
                print(f"      {script.string[:300]}...")
                
                # Intentar extraer JSON
                try:
                    start = script.string.find('{')
                    end = script.string.rfind('}') + 1
                    if start >= 0 and end > start:
                        json_str = script.string[start:end]
                        data = json.loads(json_str)
                        print(f"      ✅ JSON extraído!")
                        print(f"      Keys: {list(data.keys())[:10]}")
                except:
                    pass
    
    # Buscar meta tags con API info
    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        if meta.get('name') in ['api-url', 'api-endpoint', 'base-url']:
            print(f"\n   ✅ Meta tag encontrado: {meta}")
    
except Exception as e:
    print(f"   Error: {e}")

print()
print("5️⃣ Probando endpoint de autocompletado...")
print()

# Muchos sitios tienen endpoint de autocompletado que es más simple
autocomplete_urls = [
    'https://www.cotodigital.com.ar/api/autocomplete?q=leche',
    'https://www.cotodigital.com.ar/sitios/cdigi/api/autocomplete?term=leche',
    'https://www.cotodigital.com.ar/api/suggestions?q=leche',
]

for url in autocomplete_urls:
    try:
        r = session.get(url, timeout=5)
        print(f"   URL: {url}")
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            print(f"   Response: {r.text[:200]}...")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()

print("="*80)
print("🏁 INVESTIGACIÓN COMPLETADA")
print("="*80)
