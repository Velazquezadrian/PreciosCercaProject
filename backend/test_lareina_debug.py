from productos.scrapers.scraper_lareina import ScraperLaReina

s = ScraperLaReina()
categoria = '01020100'  # Lácteos
url = f"{s.base_url}/productosnl.asp?nl={categoria}&TM=cx"

print(f'Probando URL: {url}')
soup = s.hacer_request(url)

if soup:
    print('✅ Request exitoso')
    
    # Buscar productos
    productos_html = soup.find_all('li', {'class': 'cuadProd'})
    print(f'Productos encontrados en página: {len(productos_html)}')
    
    if productos_html:
        print('\nPrimer producto:')
        producto = productos_html[0]
        print(producto.prettify()[:500])
        
        texto = producto.get_text()
        print(f'\nTexto del producto: {texto}')
        print(f'Contiene "leche": {"leche" in texto.lower()}')
else:
    print('❌ Request falló')
