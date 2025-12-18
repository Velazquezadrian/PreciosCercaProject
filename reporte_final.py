import json

print('='*80)
print('ESTADO FINAL DEL CATÁLOGO - PreciosCerca')
print('='*80)
print()

cache = json.load(open('backend/productos_cache.json', encoding='utf-8'))
supermercados = cache.get('productos', {})

# Calcular totales
data = []
total_general = 0
for s, p in sorted(supermercados.items()):
    count = len(p)
    total_general += count
    data.append((s, count))

# Mostrar tabla
print(f'{"Supermercado":<15} {"Productos":>12} {"% del Total":>12} {"Estado":>15}')
print('-' * 80)

for s, count in sorted(data, key=lambda x: x[1], reverse=True):
    pct = (count / total_general * 100) if total_general > 0 else 0
    
    # Determinar estado
    if count > 20000:
        estado = '🥇 EXCELENTE'
    elif count > 5000:
        estado = '✅ Muy Bueno'
    elif count > 2500:
        estado = '✅ Bueno'
    elif count > 1500:
        estado = '⚠️ Mejorable'
    else:
        estado = '❌ Bajo'
    
    print(f'{s.upper():<15} {count:>12,} {pct:>11.1f}% {estado:>15}')

print('-' * 80)
print(f'{"TOTAL":<15} {total_general:>12,} {100.0:>11.1f}%')
print()

# Comparación con inicio de sesión
print('='*80)
print('EVOLUCIÓN DEL PROYECTO')
print('='*80)
print()
print(f'Inicio de sesión:     14,207 productos')
print(f'Estado actual:        {total_general:,} productos')
print(f'Mejora:               +{total_general - 14207:,} productos ({((total_general - 14207) / 14207 * 100):.0f}% más)')
print()

# Desglose de incrementos
print('='*80)
print('INCREMENTOS POR SUPERMERCADO')
print('='*80)
print()

inicial = {
    'carrefour': 6274,
    'coto': 718,
    'dia': 2918,
    'lagallega': 1740,
    'lareina': 2557
}

for s, count in sorted(data, key=lambda x: x[1], reverse=True):
    inicial_count = inicial.get(s.lower(), 0)
    diff = count - inicial_count
    if diff > 0:
        pct_change = (diff / inicial_count * 100) if inicial_count > 0 else 0
        print(f'{s.upper():<15}: {inicial_count:>8,} → {count:>8,} (+{diff:>8,} | +{pct_change:>6.0f}%)')
    elif diff < 0:
        pct_change = (abs(diff) / inicial_count * 100) if inicial_count > 0 else 0
        print(f'{s.upper():<15}: {inicial_count:>8,} → {count:>8,} ({diff:>8,} | -{pct_change:>6.0f}%)')
    else:
        print(f'{s.upper():<15}: {count:>8,} (sin cambios)')
