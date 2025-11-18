#!/usr/bin/env python3
"""
Mapeo completo de categorías y subcategorías de La Gallega
===========================================================

Descubre TODAS las categorías y subcategorías válidas.
"""

import requests
from bs4 import BeautifulSoup
import time

def probar_categoria(nl_code: str) -> tuple:
    """Prueba si una categoría existe y tiene productos"""
    url = f"https://www.lagallega.com.ar/productosnl.asp?nl={nl_code}&TM=cx"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return (False, 0)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', class_='cuadProd')
        return (len(productos) > 0, len(productos))
            
    except Exception:
        return (False, 0)

print("🔍 Mapeando TODAS las categorías de La Gallega...")
print("=" * 70)

todas_categorias = []

# Fase 1: Categorías de nivel 1 (8 dígitos)
print("\n1️⃣ Probando categorías nivel 1 (formato: XX000000)...")
for i in range(2, 25):  # Probar del 02 al 24
    nl_code = f"{str(i).zfill(2)}000000"
    existe, cant = probar_categoria(nl_code)
    
    if existe:
        todas_categorias.append(nl_code)
        print(f"   ✅ {nl_code}: {cant} prods")
    
    time.sleep(0.3)

print(f"\n   📊 Categorías nivel 1: {len([c for c in todas_categorias if len(c) == 8])}")

# Fase 2: Subcategorías nivel 2 (11 dígitos) - Patrón XX0X0000000
print("\n2️⃣ Probando subcategorías nivel 2 (formato: XX0X0000000)...")
for cat_principal in range(2, 25):  # 02 a 24
    for subcat in range(0, 10):  # 00 a 09
        nl_code = f"{str(cat_principal).zfill(2)}0{subcat}0000000"
        existe, cant = probar_categoria(nl_code)
        
        if existe:
            todas_categorias.append(nl_code)
            print(f"   ✅ {nl_code}: {cant} prods")
        
        time.sleep(0.2)

print(f"\n   📊 Subcategorías nivel 2: {len([c for c in todas_categorias if len(c) == 11])}")

print(f"\n📊 RESUMEN FINAL:")
print(f"   Total categorías encontradas: {len(todas_categorias)}")
print(f"\n   Categorías nivel 1 (8 dígitos): {[c for c in todas_categorias if len(c) == 8]}")
print(f"\n   Subcategorías nivel 2 (11 dígitos):")
for c in [cat for cat in todas_categorias if len(cat) == 11]:
    print(f"      {c}")

# Generar código Python para scraper
print("\n" + "=" * 70)
print("📝 CÓDIGO PARA COPIAR AL SCRAPER:")
print("=" * 70)
print("\ncategorias_conocidas = [")
for cat in todas_categorias:
    print(f'    "{cat}",')
print("]")

print(f"\n✅ Total de categorías para agregar: {len(todas_categorias)}")
