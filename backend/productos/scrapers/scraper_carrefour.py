# Scraper para Carrefour usando API VTEX
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
    
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []
        
        try:
            # Si la búsqueda tiene múltiples palabras, usar solo la primera
            # ya que la API de Carrefour no acepta búsquedas con espacios
            palabras = query.strip().split()
            query_api = palabras[0] if palabras else query
            
            # Buscar usando VTEX API
            params = {
                'ft': query_api,  # Full text search
                '_from': 0,
                '_to': 49     # Primeros 50 resultados
            }
            
            print(f"[Carrefour] Buscando: '{query}' (usando en API: '{query_api}')")
            response = self.session.get(self.api_search_url, params=params, timeout=15)
            print(f"[Carrefour] Status: {response.status_code}")
            
            # Status 200 y 206 (partial content) son válidos para VTEX
            if response.status_code not in [200, 206]:
                print(f"[Carrefour] Error status code: {response.status_code}")
                return productos
                
            # Parsear JSON de VTEX
            productos_json = response.json()
            print(f"[Carrefour] Productos encontrados en API: {len(productos_json)}")
            
            for producto_vtex in productos_json:
                try:
                    nombre = producto_vtex.get('productName', '')
                    if not nombre:
                        continue
                    
                    # Obtener precio más barato
                    items = producto_vtex.get('items', [])
                    if not items:
                        continue
                        
                    sellers = items[0].get('sellers', [])
                    if not sellers:
                        continue
                        
                    precio_info = sellers[0].get('commertialOffer', {})
                    precio = precio_info.get('Price', 0)
                    
                    # Obtener imagen del producto
                    imagen_url = None
                    images = producto_vtex.get('items', [{}])[0].get('images', [])
                    if images:
                        imagen_url = images[0].get('imageUrl', '')
                    
                    if precio > 0:
                        productos.append({
                            'nombre': nombre.strip(),
                            'precio': float(precio),
                            'supermercado': self.supermercado_nombre,
                            'url': f"{self.base_url}/{producto_vtex.get('linkText', '')}/p",
                            'imagen': imagen_url
                        })
                        
                except Exception as e:
                    print(f"Error procesando producto Carrefour: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error en búsqueda Carrefour: {e}")
        
        print(f"[Carrefour] Total productos válidos: {len(productos)}")
        return productos