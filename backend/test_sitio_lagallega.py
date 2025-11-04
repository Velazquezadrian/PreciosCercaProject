#!/usr/bin/env python3
"""
Diagnóstico del sitio web de La Gallega
"""

import requests
from bs4 import BeautifulSoup

print("🔍 Diagnosticando https://lagallega.com.ar\n")

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get('https://lagallega.com.ar', headers=headers, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Content Length: {len(response.text)} caracteres")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ver si hay productos en la página
    print("\n🔍 Buscando productos en la página principal...")
    
    # Buscar por diferentes patrones comunes
    productos_img = soup.find_all('img', limit=10)
    print(f"  📷 Imágenes encontradas: {len(productos_img)}")
    
    precios = soup.find_all(text=lambda text: '$' in str(text) if text else False, limit=10)
    print(f"  💰 Textos con '$': {len(precios)}")
    
    if precios:
        print("\n📊 Primeros precios encontrados:")
        for i, precio in enumerate(precios[:5], 1):
            print(f"  {i}. {precio.strip()}")
    
    # Buscar palabra "dulce"
    print("\n🔍 Buscando palabra 'dulce'...")
    textos_dulce = soup.find_all(text=lambda text: 'dulce' in str(text).lower() if text else False)
    print(f"  ✅ Encontrados: {len(textos_dulce)} resultados")
    
    if textos_dulce:
        print("\n📝 Primeros resultados con 'dulce':")
        for i, texto in enumerate(textos_dulce[:5], 1):
            print(f"  {i}. {texto.strip()[:100]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
