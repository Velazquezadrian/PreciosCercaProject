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
            # Buscar usando VTEX API
            params = {
                'ft': query,  # Full text search
                '_from': 0,
                '_to': 49     # Primeros 50 resultados
            }
            
            response = self.session.get(self.api_search_url, params=params, timeout=15)
            # Status 200 y 206 (partial content) son válidos para VTEX
            if response.status_code not in [200, 206]:
                return productos
                
            # Parsear JSON de VTEX
            productos_json = response.json()
            
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
                    
                    if precio > 0:
                        productos.append({
                            'nombre': nombre.strip(),
                            'precio': float(precio),
                            'supermercado': self.supermercado_nombre,
                            'url': f"{self.base_url}/{producto_vtex.get('linkText', '')}/p"
                        })
                        
                except Exception as e:
                    print(f"Error procesando producto Carrefour: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error en búsqueda Carrefour: {e}")
            
        return productos