#!/usr/bin/env python3
"""
Scraper para supermercado Día % con 122 categorías
Utiliza la API de búsqueda de productos de Día Argentina
"""

from .base_scraper import BaseScraper
from typing import List, Dict
import requests
import json

class ScraperDia(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://diaonline.supermercadosdia.com.ar",
            supermercado_nombre="Día %"
        )
        # API endpoint para búsqueda de productos
        self.api_url = "https://diaonline.supermercadosdia.com.ar/api/catalog_system/pub/products/search"
        
        # 122 categorías extraídas del árbol completo de Día
        # Similar a La Reina (212 cats) y La Gallega (136 cats)
        self.categorias = [
            1, 2, 16, 21, 25, 36, 42, 48, 53, 54,
            57, 63, 68, 71, 72, 76, 80, 81, 89, 95,
            103, 110, 121, 122, 132, 139, 146, 148, 154, 159,
            164, 165, 169, 172, 178, 182, 185, 193, 199, 200,
            201, 207, 209, 212, 213, 214, 215, 216, 217, 223,
            228, 233, 244, 248, 252, 256, 257, 265, 270, 276,
            280, 282, 283, 293, 297, 304, 308, 312, 321, 329,
            334, 335, 336, 337, 338, 339, 340, 344, 350, 354,
            359, 362, 366, 367, 375, 377, 378, 385, 396, 431,
            432, 436, 438, 439, 440, 441, 442, 444, 448, 450,
            461, 462, 10017, 10020, 10030, 10045, 10058, 10064, 10081, 10086,
            10098, 10099, 10110, 10113, 10119, 10121, 10123, 10128, 10132, 10133,
            10136, 10146,
        ]
        
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Busca productos en TODAS las 122 categorías de Día
        Similar a la estrategia de La Reina y La Gallega
        """
        productos_dict = {}  # Usar dict para evitar duplicados por nombre
        
        try:
            # Preparar queries: buscar con palabras en orden inverso para multi-palabra
            palabras = query.strip().split()
            queries_a_buscar = []
            
            if len(palabras) > 1:
                # Búsqueda multi-palabra: palabras en orden inverso
                # Priorizar palabras menos comunes primero
                queries_a_buscar.extend(reversed(palabras))
            else:
                # Búsqueda simple: solo una query
                queries_a_buscar.append(query.strip())
            
            print(f"[Día %] Buscando '{query}' en {len(self.categorias)} categorías")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': self.base_url
            }
            
            # Buscar con cada query
            for query_api in queries_a_buscar:
                # Buscar en cada categoría
                for categoria_id in self.categorias:
                    try:
                        # Parámetros de búsqueda con filtro de categoría
                        params = {
                            'fq': f'C:/{categoria_id}/',  # Filtro de categoría VTEX
                            'ft': query_api,
                            '_from': 0,
                            '_to': 9  # Solo 10 productos por categoría
                        }
                        
                        response = requests.get(
                            self.api_url,
                            params=params,
                            headers=headers,
                            timeout=10
                        )
                        
                        # Aceptar 200 y 206 (partial content)
                        if response.status_code not in [200, 206]:
                            continue
                        
                        data = response.json()
                        
                        if not data:
                            continue
                        
                        # Procesar productos encontrados
                        for item in data:
                            try:
                                nombre = item.get('productName', '')
                                if not nombre:
                                    continue
                                
                                # Evitar duplicados por nombre
                                if nombre in productos_dict:
                                    continue
                                
                                # Obtener precio del primer SKU disponible
                                items = item.get('items', [])
                                if not items:
                                    continue
                                
                                sellers = items[0].get('sellers', [])
                                if not sellers:
                                    continue
                                
                                precio = sellers[0].get('commertialOffer', {}).get('Price', 0)
                                precio = float(precio)
                                
                                # Obtener imagen del producto
                                imagen_url = None
                                images = items[0].get('images', [])
                                if images:
                                    imagen_url = images[0].get('imageUrl', '')
                                
                                if precio > 0:
                                    productos_dict[nombre] = {
                                        'nombre': nombre,
                                        'precio': precio,
                                        'supermercado': self.supermercado_nombre,
                                        'url': item.get('link', self.base_url),
                                        'imagen': imagen_url
                                    }
                                    
                                    # Terminar si ya tenemos 50 productos
                                    if len(productos_dict) >= 50:
                                        print(f"[Día %] Límite de 50 productos alcanzado")
                                        return list(productos_dict.values())
                            
                            except (KeyError, IndexError, ValueError):
                                continue
                    
                    except Exception as e:
                        continue
                
                # Terminar búsqueda si ya tenemos suficientes productos
                if len(productos_dict) >= 50:
                    break
            
        except Exception as e:
            print(f"[Día %] Error en búsqueda: {e}")
        
        return list(productos_dict.values())
        print(f"[Día %] Total productos encontrados: {len(productos_lista)}")
        return productos_lista
