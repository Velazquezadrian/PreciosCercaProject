#!/usr/bin/env python3
"""
Contar productos en homepage de CotoDigital
"""
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
})

print("🏠 HOMEPAGE DE COTODIGITAL.COM.AR")
print("="*80)

r = session.get('https://www.cotodigital.com.ar/', timeout=15)
print(f"Status: {r.status_code}")

soup = BeautifulSoup(r.text, 'html.parser')
print(f"Title: {soup.title.string if soup.title else 'N/A'}")

# Es una SPA, así que el contenido se carga con JavaScript
print(f"\nDivs en HTML inicial: {len(soup.find_all('div'))}")
print(f"Scripts: {len(soup.find_all('script'))}")

# Buscar si hay productos pre-renderizados
productos_prerender = soup.find_all(class_=lambda x: x and 'product' in str(x).lower())
print(f"Productos pre-renderizados: {len(productos_prerender)}")

print("\n📊 CATÁLOGO COMPLETO")
print("="*80)

# Probar endpoint de catálogo completo (sin búsqueda)
catalog_url = 'https://www.cotodigital.com.ar/sitios/cdigi/browse?format=json'
r2 = session.get(catalog_url, timeout=15)

if r2.status_code == 200:
    data = r2.json()
    
    try:
        results_list = data['contents'][0]['MainContent'][1]['contents'][0]
        
        if 'totalNumRecs' in results_list:
            print(f"✅ Total de productos en catálogo: {results_list['totalNumRecs']:,}")
        
        records = results_list.get('records', [])
        print(f"✅ Productos en esta página: {len(records)}")
        
        # Info de paginación
        if 'firstRecNum' in results_list and 'lastRecNum' in results_list:
            print(f"   Mostrando del {results_list['firstRecNum']} al {results_list['lastRecNum']}")
        
        if 'recsPerPage' in results_list:
            print(f"   Registros por página: {results_list['recsPerPage']}")
            
    except Exception as e:
        print(f"Error parseando: {e}")
else:
    print(f"Error HTTP: {r2.status_code}")

print("\n" + "="*80)
