# Scraper para Carrefour usando API VTEX con 148 categorías
from .base_scraper import BaseScraper
from typing import List, Dict
import json

class ScraperCarrefour(BaseScraper):
    def __init__(self):
        # VTEX API endpoint para búsquedas
        super().__init__(
            base_url="https://www.carrefour.com.ar",
            supermercado_nombre="Carrefour"
        )
        self.api_search_url = "https://www.carrefour.com.ar/api/catalog_system/pub/products/search"
        
        # 148 categorías extraídas del árbol completo de Carrefour
        # Similar a La Reina (212 cats) y La Gallega (136 cats)
        self.categorias = [
            1, 3, 4, 7, 11, 15, 20, 25, 31, 42,
            48, 56, 62, 71, 72, 88, 138, 148, 157, 161,
            162, 168, 172, 176, 183, 190, 195, 199, 206, 208,
            214, 222, 223, 229, 232, 233, 238, 242, 246, 250,
            255, 256, 257, 262, 266, 273, 277, 283, 286, 290,
            291, 292, 293, 299, 302, 303, 304, 305, 306, 307,
            308, 309, 310, 318, 321, 322, 323, 324, 326, 327,
            329, 330, 331, 332, 333, 334, 336, 337, 340, 344,
            345, 346, 347, 348, 349, 350, 352, 356, 358, 359,
            360, 367, 376, 377, 384, 385, 386, 387, 390, 394,
            402, 403, 412, 418, 422, 427, 435, 438, 443, 444,
            445, 451, 452, 453, 458, 462, 466, 467, 468, 469,
            470, 471, 472, 473, 474, 475, 498, 499, 514, 525,
            564, 600, 605, 606, 607, 608, 635, 636, 637, 640,
            650, 658, 665, 666, 667, 668, 669, 686,
        ]
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Busca productos en TODAS las 148 categorías de Carrefour
        Similar a la estrategia de La Reina y La Gallega
        """
        productos_dict = {}  # Usar dict para evitar duplicados por nombre
        
        try:
            # Si la búsqueda tiene múltiples palabras, usar solo la primera
            palabras = query.strip().split()
            query_api = palabras[0] if palabras else query
            
            print(f"[Carrefour] Buscando '{query}' en {len(self.categorias)} categorías")
            
            # Buscar en cada categoría
            for categoria_id in self.categorias:
                try:
                    # Buscar usando VTEX API con filtro de categoría
                    params = {
                        'fq': f'C:/{categoria_id}/',  # Filtro de categoría VTEX
                        'ft': query_api,
                        '_from': 0,
                        '_to': 9  # Solo 10 productos por categoría para no saturar
                    }
                    
                    response = self.session.get(
                        self.api_search_url, 
                        params=params, 
                        timeout=10
                    )
                    
                    # Status 200 y 206 (partial content) son válidos
                    if response.status_code not in [200, 206]:
                        continue
                    
                    productos_json = response.json()
                    
                    if not productos_json:
                        continue
                    
                    # Procesar productos encontrados
                    for producto_vtex in productos_json:
                        try:
                            nombre = producto_vtex.get('productName', '')
                            if not nombre:
                                continue
                            
                            # Evitar duplicados por nombre
                            if nombre in productos_dict:
                                continue
                            
                            # Obtener precio
                            items = producto_vtex.get('items', [])
                            if not items:
                                continue
                            
                            sellers = items[0].get('sellers', [])
                            if not sellers:
                                continue
                            
                            precio_info = sellers[0].get('commertialOffer', {})
                            precio = precio_info.get('Price', 0)
                            
                            # Obtener imagen
                            imagen_url = None
                            images = items[0].get('images', [])
                            if images:
                                imagen_url = images[0].get('imageUrl', '')
                            
                            if precio > 0:
                                productos_dict[nombre] = {
                                    'nombre': nombre.strip(),
                                    'precio': float(precio),
                                    'supermercado': self.supermercado_nombre,
                                    'url': f"{self.base_url}/{producto_vtex.get('linkText', '')}/p",
                                    'imagen': imagen_url
                                }
                                
                                # Terminar si ya tenemos 50 productos
                                if len(productos_dict) >= 50:
                                    print(f"[Carrefour] Límite de 50 productos alcanzado")
                                    return list(productos_dict.values())
                            
                        except Exception as e:
                            continue
                    
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"[Carrefour] Error en búsqueda: {e}")
        
        productos_lista = list(productos_dict.values())
        print(f"[Carrefour] Total productos encontrados: {len(productos_lista)}")
        return productos_lista