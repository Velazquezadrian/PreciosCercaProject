#!/usr/bin/env python3
"""
Descomprimir respuestas Brotli de Coto
"""
import requests
import brotli
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html, */*',
    'Accept-Language': 'es-AR,es;q=0.9',
    'Referer': 'https://www.cotodigital.com.ar/',
})

print("🔍 DESCOMPRIMIENDO RESPUESTAS DE COTO")
print("="*80)
print()

# Cargar página principal
session.get('https://www.cotodigital.com.ar/')

urls = [
    ('https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=50', 'Browse leche'),
    ('https://www.cotodigital.com.ar/sitios/cdigi/api/autocomplete?term=leche', 'Autocomplete'),
]

for url, nombre in urls:
    print(f"📍 {nombre}")
    print(f"   URL: {url}")
    
    try:
        # NO aceptar compresión primero
        headers_no_compress = session.headers.copy()
        headers_no_compress['Accept-Encoding'] = 'identity'
        
        r = session.get(url, headers=headers_no_compress, timeout=10)
        
        print(f"   Status: {r.status_code}")
        print(f"   Content-Type: {r.headers.get('content-type')}")
        print(f"   Content-Encoding: {r.headers.get('content-encoding', 'none')}")
        print(f"   Content-Length: {len(r.content)} bytes")
        
        if r.status_code == 200:
            # Intentar como JSON
            try:
                data = r.json()
                print(f"   ✅ JSON VÁLIDO!")
                print(f"   Tipo: {type(data)}")
                if isinstance(data, dict):
                    print(f"   Keys: {list(data.keys())}")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])
            except:
                # Intentar como HTML
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, 'html.parser')
                print(f"   HTML - Title: {soup.title.string if soup.title else 'N/A'}")
                print(f"   Divs: {len(soup.find_all('div'))}")
                print(f"   Scripts: {len(soup.find_all('script'))}")
                print(f"   Texto visible: {soup.get_text(strip=True)[:200]}")
                
                # Buscar si hay datos JSON embebidos
                scripts = soup.find_all('script', type='application/json')
                if scripts:
                    print(f"   ✅ {len(scripts)} scripts JSON encontrados!")
                    for idx, script in enumerate(scripts):
                        try:
                            data = json.loads(script.string)
                            print(f"   Script #{idx}:")
                            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                        except:
                            print(f"   Script #{idx}: No parseable")
        
        print()
        print("-"*80)
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print()

print()
print("🔍 PROBANDO ORACLE ENDECA (motor de búsqueda que usa Coto)")
print("="*80)
print()

# Coto parece usar Oracle Endeca (_Ntt, _Nrpp son parámetros de Endeca)
# Intentar obtener resultados en formato JSON
endeca_urls = [
    'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20&format=json',
    'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20&contentType=json',
    'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20&output=json',
    'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20&_dyncharset=UTF-8&_D%3A_dyncharset=+&format=json',
]

headers_json = session.headers.copy()
headers_json['Accept'] = 'application/json'
headers_json['Accept-Encoding'] = 'identity'

for url in endeca_urls:
    try:
        r = session.get(url, headers=headers_json, timeout=10)
        print(f"URL: {url}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"✅ JSON!")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:800])
            except:
                print(f"HTML/Texto: {r.text[:150]}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
