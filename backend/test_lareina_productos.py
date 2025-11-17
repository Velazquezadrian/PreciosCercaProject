import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Buscar divs de productos (patrón común en sitios legacy)
productos_divs = soup.find_all('div', {'class': re.compile(r'.*prod.*', re.I)})
print(f'Divs con "prod" en clase: {len(productos_divs)}')

# Buscar por ID o clase específica
todos_divs = soup.find_all('div', id=True)
print(f'Divs con ID: {len(todos_divs)}')
if todos_divs:
    print('\nPrimeros 5 IDs:')
    for div in todos_divs[:5]:
        print(f'  - ID: {div.get("id")} | Texto: {div.get_text().strip()[:50]}')

# Buscar imágenes de productos específicamente
imagenes_productos = soup.find_all('img', {'src': re.compile(r'.*Articulos.*', re.I)})
print(f'\nImágenes de artículos: {len(imagenes_productos)}')

if imagenes_productos:
    print('\nPrimeros 3 productos:')
    for img in imagenes_productos[:3]:
        # Buscar el contenedor padre
        padre = img.find_parent('div')
        if padre:
            texto = padre.get_text()
            precio_match = re.search(r'\$[\d.,]+', texto)
            print(f'\n  Imagen: {img.get("src")[:60]}')
            print(f'  Texto del div padre: {texto.strip()[:100]}')
            print(f'  Precio encontrado: {precio_match.group() if precio_match else "No"}')
