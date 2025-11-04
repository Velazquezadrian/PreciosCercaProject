#!/usr/bin/env python3
"""
Buscar endpoint API de La Gallega mediante análisis de peticiones
"""

import requests
from bs4 import BeautifulSoup
import re

print("🔍 Analizando La Gallega para encontrar endpoints de datos\n")

base_url = "https://lagallega.com.ar"

# Probar diferentes URLs que podrían tener productos
posibles_urls = [
    f"{base_url}/Articulos.asp?PA=L",
    f"{base_url}/Articulos.asp",
    f"{base_url}/productos.asp",
    f"{base_url}/buscar.asp",
    f"{base_url}/api/productos",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': base_url,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

for url in posibles_urls:
    try:
        print(f"📡 Probando: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar divs con clase que sugiera productos
            divs_producto = soup.find_all('div', class_=re.compile(r'prod|item|article|card', re.IGNORECASE))
            print(f"  📦 Divs de productos encontrados: {len(divs_producto)}")
            
            # Buscar scripts que puedan tener URLs de API
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and ('ajax' in script.string.lower() or 'load' in script.string.lower()):
                    # Buscar URLs en el script
                    urls_en_script = re.findall(r'["\']([^"\']*\.asp[^"\']*)["\']', script.string)
                    if urls_en_script:
                        print(f"  🔗 URLs encontradas en scripts:")
                        for u in set(urls_en_script[:5]):
                            print(f"     - {u}")
        else:
            print(f"  ❌ Status: {response.status_code}")
        
        print()
        
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

# Buscar el iframe o div que carga los productos
print("\n🔍 Buscando iframe o contenedor de productos en página principal...\n")
try:
    response = requests.get(base_url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar iframes
    iframes = soup.find_all('iframe')
    print(f"📺 iframes encontrados: {len(iframes)}")
    for iframe in iframes:
        src = iframe.get('src', '')
        if src:
            print(f"  - {src}")
    
    # Buscar divs con id relevante
    print("\n📦 Divs con IDs importantes:")
    divs_importantes = soup.find_all('div', id=re.compile(r'article|product|item|ticket', re.IGNORECASE))
    for div in divs_importantes:
        print(f"  - ID: {div.get('id')}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ Análisis completo")
