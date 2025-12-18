#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche&_Nrpp=20'
r = requests.get(url)

print('Status:', r.status_code)
print('URL:', r.url)

soup = BeautifulSoup(r.text, 'html.parser')

print('\n=== ESTRUCTURA ===')
print(f'Total divs: {len(soup.find_all("div"))}')
print(f'Total articles: {len(soup.find_all("article"))}')
print(f'Total li: {len(soup.find_all("li"))}')
print(f'Total span: {len(soup.find_all("span"))}')

print('\n=== CLASES COMUNES ===')
divs_con_clase = [d.get('class') for d in soup.find_all('div', limit=30) if d.get('class')]
for clase in divs_con_clase[:10]:
    print(f'  {clase}')

print('\n=== TEXTO VISIBLE (primeros 1000 chars) ===')
texto = soup.get_text(strip=True)
print(texto[:1000])

print('\n=== HTML SNIPPET ===')
print(r.text[:2000])
