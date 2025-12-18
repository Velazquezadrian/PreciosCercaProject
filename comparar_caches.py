import json

cache_root = json.load(open('productos_cache.json', encoding='utf-8'))
cache_backend = json.load(open('backend/productos_cache.json', encoding='utf-8'))

print('='*80)
print('COMPARACIÓN DE CACHES')
print('='*80)
print()

print('📁 ROOT (productos_cache.json - precarga nueva):')
for s, p in sorted(cache_root['productos'].items()):
    print(f'   {s.upper()}: {len(p):,} productos')
total_root = sum(len(p) for p in cache_root['productos'].values())
print(f'   TOTAL: {total_root:,} productos')

print()
print('📁 BACKEND (backend/productos_cache.json - servidor Flask):')
for s, p in sorted(cache_backend['productos'].items()):
    print(f'   {s.upper()}: {len(p):,} productos')
total_backend = sum(len(p) for p in cache_backend['productos'].values())
print(f'   TOTAL: {total_backend:,} productos')

print()
print('='*80)
print('ANÁLISIS:')
print('='*80)

# Comparar cada supermercado
for super_name in set(list(cache_root['productos'].keys()) + list(cache_backend['productos'].keys())):
    root_count = len(cache_root['productos'].get(super_name, {}))
    backend_count = len(cache_backend['productos'].get(super_name, {}))
    
    if root_count > backend_count:
        diff = root_count - backend_count
        print(f'✅ {super_name.upper()}: ROOT tiene +{diff:,} productos más')
    elif backend_count > root_count:
        diff = backend_count - root_count
        print(f'⚠️  {super_name.upper()}: BACKEND tiene +{diff:,} productos más')
    else:
        print(f'✓ {super_name.upper()}: Ambos iguales ({root_count:,})')
