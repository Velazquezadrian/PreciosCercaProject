"""
Script MAESTRO para precargar TODOS los supermercados
Ejecuta las 4 precargas en secuencia
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("="*80)
print("🚀 PRECARGA COMPLETA DE TODOS LOS SUPERMERCADOS")
print("="*80)
print()
print("Este script ejecutará:")
print("  1. La Gallega (136 categorías) - ~10-15 min")
print("  2. Carrefour (16 categorías) - ~2-3 min")
print("  3. Día % (16 categorías) - ~2-3 min")
print("  4. La Reina (9 categorías) - ~3-5 min")
print()
print("⏱️  Tiempo total estimado: 20-25 minutos")
print("⚠️  Solo se hace UNA VEZ, luego búsquedas instantáneas en TODOS")
print()
input("Presiona ENTER para comenzar...")
print()

# Importar los módulos de precarga
from precargar_lagallega import precargar_catalogo_completo as precargar_lagallega
from precargar_carrefour import precargar_carrefour
from precargar_dia import precargar_dia
from precargar_lareina import precargar_lareina

total_inicio = __import__('time').time()

# 1. La Gallega
print("\n" + "="*80)
print("1/4 - LA GALLEGA")
print("="*80)
try:
    precargar_lagallega()
    print("✅ La Gallega completado")
except Exception as e:
    print(f"❌ Error en La Gallega: {e}")

# 2. Carrefour
print("\n" + "="*80)
print("2/4 - CARREFOUR")
print("="*80)
try:
    precargar_carrefour()
    print("✅ Carrefour completado")
except Exception as e:
    print(f"❌ Error en Carrefour: {e}")

# 3. Día %
print("\n" + "="*80)
print("3/4 - DÍA %")
print("="*80)
try:
    precargar_dia()
    print("✅ Día % completado")
except Exception as e:
    print(f"❌ Error en Día %: {e}")

# 4. La Reina
print("\n" + "="*80)
print("4/4 - LA REINA")
print("="*80)
try:
    precargar_lareina()
    print("✅ La Reina completado")
except Exception as e:
    print(f"❌ Error en La Reina: {e}")

total_tiempo = __import__('time').time() - total_inicio

# Resumen final
from cache_manager import cache_manager
totales = {
    'lagallega': len(cache_manager.cache['productos'].get('lagallega', {})),
    'carrefour': len(cache_manager.cache['productos'].get('carrefour', {})),
    'dia': len(cache_manager.cache['productos'].get('dia', {})),
    'lareina': len(cache_manager.cache['productos'].get('lareina', {}))
}

print("\n" + "="*80)
print("🎉 PRECARGA COMPLETA FINALIZADA - TODOS LOS SUPERMERCADOS")
print("="*80)
print()
print(f"⏱️  Tiempo total: {int(total_tiempo // 60)} minutos {int(total_tiempo % 60)} segundos")
print()
print("📊 PRODUCTOS POR SUPERMERCADO:")
print(f"  🛒 La Gallega: {totales['lagallega']} productos")
print(f"  🛒 Carrefour:  {totales['carrefour']} productos")
print(f"  🛒 Día %:      {totales['dia']} productos")
print(f"  🛒 La Reina:   {totales['lareina']} productos")
print()
total_productos = sum(totales.values())
print(f"📦 TOTAL: {total_productos} productos en caché")
print()
print("🚀 TODAS las búsquedas ahora son INSTANTÁNEAS!")
print("💾 Archivo: productos_cache.json")
print()
