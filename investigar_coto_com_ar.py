#!/usr/bin/env python3
"""
Investigar cuántos productos tiene www.coto.com.ar (sin 'digital')
"""
import requests
from bs4 import BeautifulSoup
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-AR,es;q=0.9',
})

print("="*80)
print("🔍 INVESTIGANDO www.coto.com.ar")
print("="*80)
print()

# 1. Página principal
print("1️⃣ Cargando página principal...")
try:
    r = session.get('https://www.coto.com.ar/', timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   URL final: {r.url}")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f"   Title: {soup.title.string if soup.title else 'N/A'}")
        
        # Buscar productos
        productos = soup.find_all(class_=lambda x: x and 'product' in str(x).lower())
        print(f"   Elementos con 'product' en class: {len(productos)}")
        
        # Buscar grilla de productos
        items = soup.find_all('article') or soup.find_all('li', class_=lambda x: x and 'item' in str(x).lower())
        print(f"   Articles/items: {len(items)}")
        
except Exception as e:
    print(f"   Error: {e}")

print()

# 2. Probar búsqueda
print("2️⃣ Probando búsqueda de 'leche'...")
search_urls = [
    'https://www.coto.com.ar/buscar?texto=leche',
    'https://www.coto.com.ar/search?q=leche',
    'https://www.coto.com.ar/productos?search=leche',
]

for url in search_urls:
    try:
        r = session.get(url, timeout=10, allow_redirects=True)
        print(f"\n   URL: {url}")
        print(f"   Status: {r.status_code}")
        print(f"   URL final: {r.url}")
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Contar productos
            productos = soup.find_all(class_=lambda x: x and 'product' in str(x).lower())
            print(f"   Productos encontrados: {len(productos)}")
            
            # Buscar clases comunes
            divs_con_clase = set()
            for div in soup.find_all('div', class_=True, limit=100):
                classes = div.get('class', [])
                if isinstance(classes, list):
                    for c in classes:
                        if any(keyword in c.lower() for keyword in ['product', 'item', 'card']):
                            divs_con_clase.add(c)
            
            if divs_con_clase:
                print(f"   Clases relevantes: {list(divs_con_clase)[:5]}")
            
    except Exception as e:
        print(f"   Error: {e}")

print()

# 3. Probar API JSON
print("3️⃣ Probando API JSON...")
api_urls = [
    'https://www.coto.com.ar/api/products?q=leche',
    'https://www.coto.com.ar/api/search?q=leche',
]

for url in api_urls:
    try:
        r = session.get(url, timeout=10)
        print(f"\n   URL: {url}")
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"   ✅ JSON válido!")
                print(f"   Keys: {list(data.keys())[:10]}")
            except:
                print(f"   ❌ No es JSON")
    except Exception as e:
        print(f"   Error: {e}")

print()
print("="*80)
print("🏁 ANÁLISIS COMPLETADO")
print("="*80)
