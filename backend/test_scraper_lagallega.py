from productos.scrapers.scraper_lagallega import ScraperLaGallega

print("🧪 Probando ScraperLaGallega...\n")

scraper = ScraperLaGallega()

# Test 1: Búsqueda simple
print("=" * 60)
print("TEST 1: Búsqueda 'leche'")
print("=" * 60)

productos = scraper.buscar_productos('leche')

print(f"\n✅ Productos encontrados: {len(productos)}\n")

if productos:
    print("📦 Primeros 10 productos:")
    for i, p in enumerate(productos[:10], 1):
        print(f"  {i}. {p['nombre'][:60]} - ${p['precio']}")
        if p.get('imagen'):
            print(f"     Imagen: {p['imagen'][:70]}")
else:
    print("⚠️ No se encontraron productos")

print(f"\n{'=' * 60}")
print("TEST 2: Búsqueda 'arroz'")
print("=" * 60)

productos2 = scraper.buscar_productos('arroz')
print(f"\n✅ Productos encontrados: {len(productos2)}\n")

if productos2:
    print("📦 Primeros 5 productos:")
    for i, p in enumerate(productos2[:5], 1):
        print(f"  {i}. {p['nombre'][:60]} - ${p['precio']}")
else:
    print("⚠️ No se encontraron productos")
