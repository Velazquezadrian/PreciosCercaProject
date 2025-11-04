#!/usr/bin/env python3
"""
Probar acceso al endpoint AJAX de La Gallega
"""

import requests
from bs4 import BeautifulSoup

print("🔍 Probando endpoint AJAX de La Gallega\n")

base_url = "https://lagallega.com.ar"
ajax_url = f"{base_url}/Articulos.asp?PA=L"

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': base_url
    }
    
    print(f"📡 Accediendo a: {ajax_url}")
    response = requests.get(ajax_url, headers=headers, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Content Length: {len(response.text)} caracteres\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar productos
    print("🔍 Buscando estructura de productos...")
    
    # Buscar precios
    import re
    precios = soup.find_all(string=re.compile(r'\$[\d.,]+'))
    print(f"💰 Precios encontrados: {len(precios)}")
    
    if precios:
        print("\n📊 Primeros 5 precios:")
        for i, precio in enumerate(precios[:5], 1):
            print(f"  {i}. {precio.strip()}")
    
    # Buscar palabra "dulce"
    print("\n🔍 Buscando productos con 'dulce'...")
    textos_dulce = soup.find_all(string=re.compile(r'dulce', re.IGNORECASE))
    print(f"✅ Encontrados: {len(textos_dulce)}")
    
    if textos_dulce:
        print("\n📝 Primeros 5 productos con 'dulce':")
        for i, texto in enumerate(textos_dulce[:5], 1):
            # Buscar el contenedor padre para obtener más info
            parent = texto.parent
            if parent:
                texto_completo = parent.get_text().strip()
                print(f"  {i}. {texto_completo[:100]}")
    
    # Ver la estructura general
    print("\n🏗️ Analizando estructura HTML...")
    divs = soup.find_all('div', limit=20)
    print(f"📦 Divs encontrados: {len(divs)}")
    
    # Buscar contenedores de productos comunes
    productos_class = soup.find_all(['div', 'article'], class_=re.compile(r'product|item|card', re.IGNORECASE))
    print(f"🛒 Elementos tipo producto: {len(productos_class)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
