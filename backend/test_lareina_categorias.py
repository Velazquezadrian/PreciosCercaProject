from productos.scrapers.scraper_lareina import ScraperLaReina

s = ScraperLaReina()
print(f'Categorías cargadas: {len(s.categorias)}')
print(f'Primeras 10: {s.categorias[:10]}')

print('\nBuscando "leche"...')
resultados = s.buscar_productos('leche')
print(f'Total encontrado: {len(resultados)}')

if resultados:
    print('\nPrimeros 5 productos:')
    for i, p in enumerate(resultados[:5], 1):
        print(f'{i}. {p["nombre"][:50]}')
        print(f'   Precio: ${p["precio"]}')
