from productos.scrapers.scraper_lareina import ScraperLaReina

s = ScraperLaReina()
print('Buscando "leche" en La Reina...')
resultados = s.buscar_productos('leche')
print(f'\nTotal encontrado: {len(resultados)}')

if resultados:
    print('\nPrimeros 5 productos:')
    for i, p in enumerate(resultados[:5], 1):
        print(f'{i}. {p["nombre"][:50]} - ${p["precio"]}')
        print(f'   Imagen: {p["imagen"][:60] if p["imagen"] else "Sin imagen"}')
else:
    print('Sin resultados')
