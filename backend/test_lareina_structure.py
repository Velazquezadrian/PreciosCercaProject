import requests
from bs4 import BeautifulSoup

# Analizar estructura de La Reina
url = 'https://www.lareinaonline.com.ar/productosnl.asp?nl=01010100&TM=cx'
r = requests.get(url)
print(f'Status: {r.status_code}')

soup = BeautifulSoup(r.content, 'html.parser')

# Buscar productos
tablas = soup.find_all('table')
print(f'\nTablas encontradas: {len(tablas)}')

imagenes = soup.find_all('img')
print(f'Imágenes encontradas: {len(imagenes)}')

# Buscar patrones de precio
precios = soup.find_all(text=lambda text: text and '$' in str(text))
print(f'\nTextos con "$": {len(precios)}')
print('Primeros 5 precios:')
for precio in precios[:5]:
    print(f'  - {precio.strip()[:60]}')

# Buscar divs o contenedores de productos
divs = soup.find_all('div', class_=True)
print(f'\nDivs con clase: {len(divs)}')
if divs:
    print('Primeras 3 clases:')
    for div in divs[:3]:
        print(f'  - {div.get("class")}')

# Buscar por estructura de tabla
trs = soup.find_all('tr')
print(f'\nFilas TR: {len(trs)}')
if trs:
    print('\nPrimera fila completa:')
    print(trs[0].prettify()[:500])
