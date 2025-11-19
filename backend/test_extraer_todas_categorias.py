#!/usr/bin/env python3
"""
Script para extraer TODAS las categorías de Carrefour y Día recursivamente
Similar a cómo se hizo con La Reina (212) y La Gallega (136)
"""

import json
from typing import List, Dict, Set

def extraer_categorias_recursivo(nodo: Dict, nivel: int = 0) -> List[Dict]:
    """
    Extrae todas las categorías de un árbol de forma recursiva
    
    Retorna lista de dicts con:
    - id: ID de categoría
    - name: Nombre de categoría
    - url: URL de categoría
    - nivel: Nivel en el árbol (0=raíz, 1=subcategoría, etc.)
    """
    categorias = []
    
    # Agregar categoría actual
    categorias.append({
        'id': nodo['id'],
        'name': nodo['name'],
        'url': nodo.get('url', ''),
        'nivel': nivel
    })
    
    # Procesar hijos recursivamente
    if 'children' in nodo and nodo['children']:
        for hijo in nodo['children']:
            categorias.extend(extraer_categorias_recursivo(hijo, nivel + 1))
    
    return categorias


def procesar_carrefour():
    """Procesa árbol de categorías de Carrefour"""
    
    print("=" * 80)
    print("🛒 CARREFOUR - Extrayendo todas las categorías")
    print("=" * 80)
    
    with open('carrefour_categorias_response.json', 'r', encoding='utf-8') as f:
        arbol = json.load(f)
    
    todas_categorias = []
    
    # Procesar cada categoría raíz
    for nodo_raiz in arbol:
        categorias_rama = extraer_categorias_recursivo(nodo_raiz)
        todas_categorias.extend(categorias_rama)
    
    # Estadísticas por nivel
    categorias_por_nivel = {}
    for cat in todas_categorias:
        nivel = cat['nivel']
        if nivel not in categorias_por_nivel:
            categorias_por_nivel[nivel] = []
        categorias_por_nivel[nivel].append(cat)
    
    print(f"\n✅ Total categorías: {len(todas_categorias)}")
    print(f"\n📊 Distribución por nivel:")
    for nivel in sorted(categorias_por_nivel.keys()):
        cats = categorias_por_nivel[nivel]
        print(f"   Nivel {nivel}: {len(cats)} categorías")
        if len(cats) <= 20:  # Mostrar solo si no son muchas
            for cat in cats[:10]:
                print(f"      - {cat['name']} (ID: {cat['id']})")
            if len(cats) > 10:
                print(f"      ... y {len(cats) - 10} más")
    
    # Guardar lista completa
    with open('carrefour_categorias_completas.json', 'w', encoding='utf-8') as f:
        json.dump(todas_categorias, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Guardado en carrefour_categorias_completas.json")
    
    # Generar código Python para scraper (solo IDs de categorías útiles para comida)
    categorias_comida = [cat for cat in todas_categorias if any(
        keyword in cat['name'].lower() 
        for keyword in ['almacén', 'almacen', 'bebida', 'lácteo', 'lacteo', 'fresco', 
                       'carne', 'verdura', 'fruta', 'panadería', 'panaderia',
                       'congelado', 'despensa', 'conserva', 'snack', 'golosina',
                       'desayuno', 'infusión', 'infusion', 'aceite', 'condimento']
    )]
    
    print(f"\n🍽️ Categorías relacionadas con comida: {len(categorias_comida)}")
    
    # Generar lista de IDs para el scraper
    ids_categorias = sorted(set(cat['id'] for cat in todas_categorias))
    print(f"\n📋 IDs únicos: {len(ids_categorias)}")
    
    # Código Python para copiar al scraper
    print(f"\n" + "="*80)
    print("📝 CÓDIGO PARA scraper_carrefour.py:")
    print("="*80)
    print(f"# Total: {len(ids_categorias)} categorías")
    print("CATEGORIAS = [")
    for i in range(0, len(ids_categorias), 10):
        batch = ids_categorias[i:i+10]
        print("    " + ", ".join(str(id) for id in batch) + ",")
    print("]")
    
    return todas_categorias, ids_categorias


def procesar_dia():
    """Procesa árbol de categorías de Día"""
    
    print("\n\n")
    print("=" * 80)
    print("🛒 DÍA % - Extrayendo todas las categorías")
    print("=" * 80)
    
    with open('dia_categorias_response.json', 'r', encoding='utf-8') as f:
        arbol = json.load(f)
    
    todas_categorias = []
    
    # Procesar cada categoría raíz
    for nodo_raiz in arbol:
        categorias_rama = extraer_categorias_recursivo(nodo_raiz)
        todas_categorias.extend(categorias_rama)
    
    # Estadísticas por nivel
    categorias_por_nivel = {}
    for cat in todas_categorias:
        nivel = cat['nivel']
        if nivel not in categorias_por_nivel:
            categorias_por_nivel[nivel] = []
        categorias_por_nivel[nivel].append(cat)
    
    print(f"\n✅ Total categorías: {len(todas_categorias)}")
    print(f"\n📊 Distribución por nivel:")
    for nivel in sorted(categorias_por_nivel.keys()):
        cats = categorias_por_nivel[nivel]
        print(f"   Nivel {nivel}: {len(cats)} categorías")
        if len(cats) <= 20:
            for cat in cats[:10]:
                print(f"      - {cat['name']} (ID: {cat['id']})")
            if len(cats) > 10:
                print(f"      ... y {len(cats) - 10} más")
    
    # Guardar lista completa
    with open('dia_categorias_completas.json', 'w', encoding='utf-8') as f:
        json.dump(todas_categorias, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Guardado en dia_categorias_completas.json")
    
    # Generar lista de IDs
    ids_categorias = sorted(set(cat['id'] for cat in todas_categorias))
    print(f"\n📋 IDs únicos: {len(ids_categorias)}")
    
    # Código Python para scraper
    print(f"\n" + "="*80)
    print("📝 CÓDIGO PARA scraper_dia.py:")
    print("="*80)
    print(f"# Total: {len(ids_categorias)} categorías")
    print("CATEGORIAS = [")
    for i in range(0, len(ids_categorias), 10):
        batch = ids_categorias[i:i+10]
        print("    " + ", ".join(str(id) for id in batch) + ",")
    print("]")
    
    return todas_categorias, ids_categorias


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║           EXTRACCIÓN COMPLETA DE CATEGORÍAS - CARREFOUR Y DÍA             ║")
    print("║                                                                            ║")
    print("║  Similar a La Reina (212 cats) y La Gallega (136 cats)                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Procesar Carrefour
    carrefour_cats, carrefour_ids = procesar_carrefour()
    
    # Procesar Día
    dia_cats, dia_ids = procesar_dia()
    
    # Resumen final
    print("\n\n")
    print("=" * 80)
    print("📊 RESUMEN FINAL")
    print("=" * 80)
    print(f"🛒 Carrefour: {len(carrefour_cats)} categorías totales, {len(carrefour_ids)} IDs únicos")
    print(f"🛒 Día %:     {len(dia_cats)} categorías totales, {len(dia_ids)} IDs únicos")
    print(f"🛒 La Reina:  212 categorías (HTML scraping)")
    print(f"🛒 La Gallega: 136 categorías (HTML scraping)")
    print(f"\n✅ TOTAL: {len(carrefour_cats) + len(dia_cats) + 212 + 136} categorías mapeadas en los 4 supermercados")
    print("=" * 80)
    print("\n")
