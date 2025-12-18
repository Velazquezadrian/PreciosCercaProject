#!/usr/bin/env python3
"""
Explorar API JSON de Coto (Oracle Endeca)
"""
import requests
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-AR,es;q=0.9',
    'Accept-Encoding': 'identity',
    'Referer': 'https://www.cotodigital.com.ar/',
})

# Cargar página principal
session.get('https://www.cotodigital.com.ar/')

print("🎉 API JSON DE COTO ENCONTRADA!")
print("="*80)
print()

# Hacer búsqueda
url = 'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=50&format=json'

r = session.get(url, timeout=10)
data = r.json()

print(f"✅ Respuesta JSON recibida")
print(f"Status: {r.status_code}")
print()

# Guardar JSON completo para análisis
with open('coto_response.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("💾 JSON completo guardado en: coto_response.json")
print()

# Explorar estructura
print("📊 ESTRUCTURA DE LA RESPUESTA:")
print(f"Keys principales: {list(data.keys())}")
print()

if 'contents' in data:
    print(f"Total contents: {len(data['contents'])}")
    
    for idx, content in enumerate(data['contents']):
        print(f"\n--- Content #{idx} ---")
        print(f"Keys: {list(content.keys())}")
        
        # Buscar donde están los productos
        for key, value in content.items():
            if isinstance(value, list) and len(value) > 0:
                print(f"\n  {key} (lista con {len(value)} items):")
                first_item = value[0]
                if isinstance(first_item, dict):
                    print(f"    Primer item keys: {list(first_item.keys())[:10]}")
                    
                    # Ver si tiene productos
                    if 'records' in first_item:
                        print(f"\n    ✅ PRODUCTOS ENCONTRADOS!")
                        records = first_item['records']
                        print(f"    Total productos: {len(records)}")
                        
                        if len(records) > 0:
                            print(f"\n    PRIMER PRODUCTO:")
                            producto = records[0]
                            print(f"    Keys: {list(producto.keys())}")
                            print()
                            
                            # Extraer campos importantes
                            campos_interesantes = [
                                'repositoryId', 'displayName', 'name', 'product.displayName',
                                'product_name', 'salePrice', 'price', 'listPrice', 
                                'product.salePrice', 'product.listPrice',
                                'imageURL', 'thumbnailImage', 'product.imageURL',
                                'productURL', 'product.url', 'url'
                            ]
                            
                            print("    CAMPOS DETECTADOS:")
                            for campo in campos_interesantes:
                                if campo in producto.get('attributes', {}):
                                    valor = producto['attributes'][campo]
                                    print(f"      {campo}: {valor}")
                            
                            print("\n    PRODUCTO COMPLETO (primeros 2000 chars):")
                            print(json.dumps(producto, indent=4, ensure_ascii=False)[:2000])
                            print()
                            
                            # Mostrar más productos
                            print(f"\n    PRIMEROS 3 PRODUCTOS:")
                            for i, prod in enumerate(records[:3]):
                                attrs = prod.get('attributes', {})
                                nombre = (attrs.get('product.displayName') or 
                                         attrs.get('displayName') or 
                                         attrs.get('name') or 
                                         'Sin nombre')
                                precio = (attrs.get('product.salePrice') or 
                                         attrs.get('salePrice') or 
                                         attrs.get('price') or 
                                         attrs.get('listPrice') or 
                                         'Sin precio')
                                print(f"      {i+1}. {nombre[0] if isinstance(nombre, list) else nombre} - ${precio}")

print("\n")
print("="*80)
print("✅ ANÁLISIS COMPLETADO")
print("="*80)
