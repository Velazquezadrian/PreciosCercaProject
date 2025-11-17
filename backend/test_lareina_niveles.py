import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Buscar imágenes de productos
imagenes_productos = soup.find_all('img', {'src': re.compile(r'.*Articulos.*', re.I)})
print(f'Total imágenes de productos: {len(imagenes_productos)}')

print('\n=== ANÁLISIS DE PRIMEROS 3 PRODUCTOS ===\n')

for i, img in enumerate(imagenes_productos[:3], 1):
    print(f'--- PRODUCTO {i} ---')
    print(f'Imagen SRC: {img.get("src")}')
    
    # Buscar en diferentes niveles de padres
    for nivel in range(1, 5):
        padre = img
        for _ in range(nivel):
            padre = padre.find_parent()
            if not padre:
                break
        
        if padre:
            # Buscar precio en este nivel
            precio_match = re.search(r'\$[\d.,]+', padre.get_text())
            if precio_match:
                print(f'\nNivel {nivel} - ENCONTRADO PRECIO: {precio_match.group()}')
                print(f'Clase del contenedor: {padre.get("class")}')
                print(f'Tag: {padre.name}')
                print(f'Texto completo: {padre.get_text().strip()[:200]}')
                break
    print()
