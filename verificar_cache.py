import json

# Leer del ROOT que es donde guarda la precarga
cache = json.load(open('productos_cache.json', encoding='utf-8'))
supermercados = cache.get('productos', {})

print('=== CACHE ACTUALIZADO ===')
print('')

total = 0
for s, p in sorted(supermercados.items()):
    count = len(p)
    print(f'{s.upper()}: {count:,} productos')
    total += count

print('')
print(f'TOTAL GENERAL: {total:,} productos')
print('')
print(f'COTO ANTES: 718 productos')
print(f'COTO AHORA: {len(supermercados.get("coto", {})):,} productos')
print(f'AUMENTO: +{len(supermercados.get("coto", {})) - 718:,} productos ({((len(supermercados.get("coto", {})) - 718) / 718 * 100):.0f}%)')
