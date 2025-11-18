#!/usr/bin/env python3
"""
Test de mapeo completo de categorías de La Reina
================================================

Similar a test_lagallega_mapeo_completo.py, este script descubre
todas las categorías válidas de La Reina mediante prueba sistemática.

Método:
1. Probar categorías nivel 1: XX000000 (01 a 30)
2. Probar subcategorías nivel 2: XX0X0000 (para cada nivel 1 válido)
3. Probar subcategorías nivel 3: XX0X0X00 (para cada nivel 2 válido)

La Reina usa: productosnl.asp?nl=XXXXXXXX (8 dígitos)
"""

import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://www.lareinaonline.com.ar"

def probar_categoria(codigo):
    """Prueba si una categoría existe y tiene productos"""
    url = f"{BASE_URL}/productosnl.asp?nl={codigo}&TM=cx"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, 0
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar productos en la página
        productos = soup.find_all('li', {'class': 'cuadProd'})
        
        # Si tiene productos, es válida
        if len(productos) > 0:
            return True, len(productos)
        
        return False, 0
    except:
        return False, 0


def descubrir_nivel_1():
    """Descubre categorías nivel 1: XX000000"""
    print("=" * 60)
    print("NIVEL 1: Categorías principales (XX000000)")
    print("=" * 60)
    
    categorias_validas = []
    
    for i in range(1, 31):  # Probar 01 a 30
        codigo = f"{i:02d}000000"
        print(f"Probando {codigo}...", end=' ', flush=True)
        
        es_valida, num_productos = probar_categoria(codigo)
        
        if es_valida:
            print(f"✅ VÁLIDA ({num_productos} productos)")
            categorias_validas.append(codigo)
        else:
            print("❌")
        
        time.sleep(0.3)  # Evitar saturar el servidor
    
    print(f"\n✅ Encontradas {len(categorias_validas)} categorías nivel 1")
    return categorias_validas


def descubrir_nivel_2(categorias_nivel1):
    """Descubre subcategorías nivel 2: XX0X0000"""
    print("\n" + "=" * 60)
    print("NIVEL 2: Subcategorías (XX0X0000)")
    print("=" * 60)
    
    todas_subcategorias = []
    
    for cat_nivel1 in categorias_nivel1:
        prefijo = cat_nivel1[:2]  # Ej: "01" de "01000000"
        print(f"\n🔍 Explorando subcategorías de {prefijo}...")
        
        subcats_encontradas = []
        
        for j in range(1, 10):  # Probar XX010000 a XX090000
            codigo = f"{prefijo}0{j}0000"
            print(f"  {codigo}...", end=' ', flush=True)
            
            es_valida, num_productos = probar_categoria(codigo)
            
            if es_valida:
                print(f"✅ ({num_productos})")
                subcats_encontradas.append(codigo)
                todas_subcategorias.append(codigo)
            else:
                print("❌")
            
            time.sleep(0.3)
        
        print(f"  Subcategorías en {prefijo}: {len(subcats_encontradas)}")
    
    print(f"\n✅ Encontradas {len(todas_subcategorias)} subcategorías nivel 2")
    return todas_subcategorias


def descubrir_nivel_3(categorias_nivel2):
    """Descubre subcategorías nivel 3: XX0X0X00"""
    print("\n" + "=" * 60)
    print("NIVEL 3: Sub-subcategorías (XX0X0X00)")
    print("=" * 60)
    
    todas_subsubcategorias = []
    
    for cat_nivel2 in categorias_nivel2:
        prefijo = cat_nivel2[:4]  # Ej: "0101" de "01010000"
        print(f"\n🔍 Explorando nivel 3 de {prefijo}...")
        
        subsubcats_encontradas = []
        
        for k in range(1, 10):  # Probar XX0X0100 a XX0X0900
            codigo = f"{prefijo}0{k}00"
            print(f"  {codigo}...", end=' ', flush=True)
            
            es_valida, num_productos = probar_categoria(codigo)
            
            if es_valida:
                print(f"✅ ({num_productos})")
                subsubcats_encontradas.append(codigo)
                todas_subsubcategorias.append(codigo)
            else:
                print("❌")
            
            time.sleep(0.3)
        
        if len(subsubcats_encontradas) > 0:
            print(f"  Nivel 3 en {prefijo}: {len(subsubcats_encontradas)}")
    
    print(f"\n✅ Encontradas {len(todas_subsubcategorias)} subcategorías nivel 3")
    return todas_subsubcategorias


def main():
    print("🔍 MAPEO COMPLETO DE CATEGORÍAS - LA REINA")
    print("=" * 60)
    print("Este proceso puede tomar 10-15 minutos...")
    print()
    
    # Paso 1: Nivel 1
    categorias_nivel1 = descubrir_nivel_1()
    
    # Paso 2: Nivel 2
    categorias_nivel2 = descubrir_nivel_2(categorias_nivel1)
    
    # Paso 3: Nivel 3
    categorias_nivel3 = descubrir_nivel_3(categorias_nivel2)
    
    # Combinar todas
    todas_categorias = categorias_nivel1 + categorias_nivel2 + categorias_nivel3
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"Nivel 1 (XX000000): {len(categorias_nivel1)} categorías")
    print(f"Nivel 2 (XX0X0000): {len(categorias_nivel2)} subcategorías")
    print(f"Nivel 3 (XX0X0X00): {len(categorias_nivel3)} sub-subcategorías")
    print(f"TOTAL: {len(todas_categorias)} categorías")
    
    # Generar código Python para copiar al scraper
    print("\n" + "=" * 60)
    print("📋 CÓDIGO PARA scraper_lareina.py:")
    print("=" * 60)
    print("categorias_conocidas = [")
    
    if categorias_nivel1:
        print("    # Nivel 1: Categorías principales")
        for cat in categorias_nivel1:
            print(f"    '{cat}',")
    
    if categorias_nivel2:
        print("    # Nivel 2: Subcategorías")
        for cat in categorias_nivel2:
            print(f"    '{cat}',")
    
    if categorias_nivel3:
        print("    # Nivel 3: Sub-subcategorías")
        for cat in categorias_nivel3:
            print(f"    '{cat}',")
    
    print("]")
    print(f"# Total: {len(todas_categorias)} categorías ({len(categorias_nivel1)} nivel 1 + {len(categorias_nivel2)} nivel 2 + {len(categorias_nivel3)} nivel 3)")


if __name__ == '__main__':
    main()
