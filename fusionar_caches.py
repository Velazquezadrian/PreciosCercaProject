#!/usr/bin/env python3
"""
Fusiona los dos caches tomando el mejor de cada supermercado
"""
import json
from datetime import datetime

print('='*80)
print('FUSIONANDO CACHES - Tomando el mejor de cada supermercado')
print('='*80)
print()

# Cargar ambos caches
cache_root = json.load(open('productos_cache.json', encoding='utf-8'))
cache_backend = json.load(open('backend/productos_cache.json', encoding='utf-8'))

# Cache unificado
cache_fusionado = {
    'last_update': datetime.now().isoformat(),
    'productos': {}
}

# Fusionar: tomar el que tenga MÁS productos por cada supermercado
supermercados = set(list(cache_root['productos'].keys()) + list(cache_backend['productos'].keys()))

for super_name in supermercados:
    root_productos = cache_root['productos'].get(super_name, {})
    backend_productos = cache_backend['productos'].get(super_name, {})
    
    root_count = len(root_productos)
    backend_count = len(backend_productos)
    
    if root_count >= backend_count:
        cache_fusionado['productos'][super_name] = root_productos
        print(f'✅ {super_name.upper()}: Tomando ROOT ({root_count:,} productos)')
    else:
        cache_fusionado['productos'][super_name] = backend_productos
        print(f'✅ {super_name.upper()}: Tomando BACKEND ({backend_count:,} productos)')

total_fusionado = sum(len(p) for p in cache_fusionado['productos'].values())

print()
print('='*80)
print(f'RESULTADO FINAL: {total_fusionado:,} productos totales')
print('='*80)
print()

# Mostrar desglose
for s, p in sorted(cache_fusionado['productos'].items()):
    print(f'   {s.upper()}: {len(p):,} productos')

print()

# Guardar cache fusionado
print('💾 Guardando cache fusionado en backend/productos_cache.json...')
with open('backend/productos_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache_fusionado, f, ensure_ascii=False, indent=2)

print('✅ Cache fusionado guardado exitosamente')
print()
print('='*80)
print('NOTA: El servidor Flask ahora tiene TODOS los productos')
print('='*80)
