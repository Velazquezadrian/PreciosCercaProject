#!/usr/bin/env python3
"""
Script para descubrir categorías de Carrefour
Similar a test_lareina_mapeo_categorias.py y test_lagallega_mapeo_completo.py

Carrefour usa VTEX API - probablemente tiene endpoints de categoría:
- /api/catalog_system/pub/category/tree
- /api/catalog_system/pub/products/search?category=X
"""

import requests
import json
from typing import List, Dict

BASE_URL = "https://www.carrefour.com.ar"

def probar_endpoint_categorias():
    """Intenta obtener árbol de categorías de Carrefour"""
    
    print("=" * 80)
    print("🔍 BUSCANDO ENDPOINT DE CATEGORÍAS EN CARREFOUR")
    print("=" * 80)
    
    # VTEX tiene varios endpoints estándar para categorías
    endpoints_posibles = [
        "/api/catalog_system/pub/category/tree/1",
        "/api/catalog_system/pub/category/tree/2",
        "/api/catalog_system/pub/category/tree/3",
        "/api/catalog_system/pub/category/tree",
        "/api/catalog/pub/category/tree",
        "/api/catalog_system/pvt/category/tree",
        "/_v/segment/graphql/v1",  # GraphQL endpoint
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    for endpoint in endpoints_posibles:
        url = BASE_URL + endpoint
        print(f"\n🔍 Probando: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ JSON válido recibido")
                    print(f"   📊 Tipo: {type(data)}")
                    
                    if isinstance(data, list):
                        print(f"   📋 Longitud: {len(data)} items")
                        if len(data) > 0:
                            print(f"   🔍 Primer item: {json.dumps(data[0], indent=2)[:300]}...")
                    elif isinstance(data, dict):
                        print(f"   🔑 Keys: {list(data.keys())}")
                        print(f"   📄 Data: {json.dumps(data, indent=2)[:500]}...")
                    
                    # Guardar respuesta exitosa
                    with open('carrefour_categorias_response.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"   💾 Guardado en carrefour_categorias_response.json")
                    
                    return data
                    
                except json.JSONDecodeError:
                    print(f"   ⚠️ Respuesta no es JSON válido")
                    print(f"   📄 Primeros 200 chars: {response.text[:200]}")
            
            elif response.status_code == 404:
                print(f"   ❌ Endpoint no existe")
            elif response.status_code == 403:
                print(f"   🔒 Acceso denegado (requiere autenticación)")
            else:
                print(f"   ⚠️ Status inesperado")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
    
    return None


def probar_busqueda_por_categoria():
    """Intenta buscar productos usando parámetros de categoría"""
    
    print("\n" + "=" * 80)
    print("🔍 PROBANDO BÚSQUEDA POR CATEGORÍA")
    print("=" * 80)
    
    # Parámetros comunes en VTEX para filtrar por categoría
    parametros_posibles = [
        {'category': '1'},
        {'category': '100'},
        {'category-1': '1'},
        {'category-2': '100'},
        {'fq': 'C:/1/'},
        {'fq': 'C:1'},
        {'fq': 'productClusterIds:1'},
        {'map': 'c'},
        {'map': 'c,c'},
    ]
    
    base_search_url = BASE_URL + "/api/catalog_system/pub/products/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    for params in parametros_posibles:
        print(f"\n🔍 Probando params: {params}")
        
        try:
            response = requests.get(base_search_url, params=params, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   URL: {response.url}")
            
            if response.status_code in [200, 206]:
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"   ✅ {len(data)} productos encontrados")
                        print(f"   📦 Primer producto: {data[0].get('productName', 'N/A')}")
                        return params, data
                    else:
                        print(f"   ⚠️ Sin resultados")
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None, []


def analizar_estructura_producto():
    """Analiza un producto de Carrefour para ver si tiene info de categoría"""
    
    print("\n" + "=" * 80)
    print("🔍 ANALIZANDO ESTRUCTURA DE PRODUCTO")
    print("=" * 80)
    
    # Buscar un producto común para analizar su estructura
    url = BASE_URL + "/api/catalog_system/pub/products/search"
    params = {'ft': 'leche', '_from': 0, '_to': 0}  # Solo 1 producto
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code in [200, 206]:
            data = response.json()
            
            if data and len(data) > 0:
                producto = data[0]
                
                print(f"\n📦 Producto encontrado: {producto.get('productName', 'N/A')}")
                print(f"\n🔑 Keys principales del producto:")
                for key in producto.keys():
                    print(f"   - {key}")
                
                # Buscar campos relacionados con categorías
                campos_categoria = ['categories', 'categoryId', 'categoryIds', 'category', 
                                   'categoryTree', 'categoryPath', 'productClusters']
                
                print(f"\n🏷️ Campos de categoría encontrados:")
                for campo in campos_categoria:
                    if campo in producto:
                        valor = producto[campo]
                        print(f"   ✅ {campo}: {json.dumps(valor, indent=2)[:200]}...")
                
                # Guardar producto completo para análisis
                with open('carrefour_producto_ejemplo.json', 'w', encoding='utf-8') as f:
                    json.dump(producto, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Producto completo guardado en carrefour_producto_ejemplo.json")
                
                return producto
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None


def probar_url_directa_categoria():
    """Intenta acceder a URLs de categoría directamente"""
    
    print("\n" + "=" * 80)
    print("🔍 PROBANDO URLs DE CATEGORÍA DIRECTAS")
    print("=" * 80)
    
    # URLs comunes de categorías en sitios web de supermercados
    urls_categorias = [
        "/almacen",
        "/lacteos",
        "/bebidas",
        "/carnes",
        "/frutas-y-verduras",
        "/limpieza",
        "/perfumeria",
        "/categoria/almacen",
        "/c/almacen",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    for url_cat in urls_categorias:
        url = BASE_URL + url_cat
        print(f"\n🔍 Probando: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Página existe!")
                print(f"   📄 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                
                # Buscar patrones en el HTML
                html = response.text
                if 'category' in html.lower():
                    print(f"   ✅ Contiene 'category' en HTML")
                if 'api/catalog' in html:
                    print(f"   ✅ Contiene 'api/catalog' en HTML")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                 MAPEO DE CATEGORÍAS - CARREFOUR                            ║")
    print("║                                                                            ║")
    print("║  Objetivo: Descubrir estructura de categorías en API de Carrefour         ║")
    print("║  Similar a La Reina (212 cats) y La Gallega (136 cats)                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # 1. Intentar obtener árbol de categorías
    categorias = probar_endpoint_categorias()
    
    # 2. Si no funciona, probar búsqueda por categoría
    if not categorias:
        params_exitosos, productos = probar_busqueda_por_categoria()
    
    # 3. Analizar estructura de producto para ver campos de categoría
    producto = analizar_estructura_producto()
    
    # 4. Probar URLs directas de categoría
    probar_url_directa_categoria()
    
    print("\n")
    print("=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print("\n📋 Revisa los archivos generados:")
    print("   - carrefour_categorias_response.json (si se encontró endpoint)")
    print("   - carrefour_producto_ejemplo.json (estructura de producto)")
    print("\n")
