#!/usr/bin/env python3
"""
Scraper para supermercado Día %
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
        
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Buscar productos en Día usando su API REST
        """
        productos = []
        
        try:
            # Parámetros de búsqueda
            params = {
                'ft': query,  # Full text search
                '_from': 0,
                '_to': 49  # Traer hasta 50 productos
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': self.base_url
            }
            
            response = requests.get(
                self.api_url,
                params=params,
                headers=headers,
                timeout=10
            )
            
            # Aceptar tanto 200 como 206 (partial content)
            if response.status_code in [200, 206]:
                data = response.json()
                
                for item in data:
                    try:
                        # Extraer información del producto
                        nombre = item.get('productName', '')
                        
                        # Obtener precio del primer SKU disponible
                        items = item.get('items', [])
                        if not items:
                            continue
                            
                        sellers = items[0].get('sellers', [])
                        if not sellers:
                            continue
                        
                        # Precio en centavos, convertir a pesos
                        precio_centavos = sellers[0].get('commertialOffer', {}).get('Price', 0)
                        precio = float(precio_centavos)
                        
                        # Obtener imagen del producto
                        imagen_url = None
                        images = items[0].get('images', [])
                        if images:
                            imagen_url = images[0].get('imageUrl', '')
                        
                        if nombre and precio > 0:
                            productos.append({
                                'nombre': nombre,
                                'precio': precio,
                                'supermercado': self.supermercado_nombre,
                                'url': item.get('link', self.base_url),
                                'imagen': imagen_url
                            })
                            
                    except (KeyError, IndexError, ValueError) as e:
                        # Saltar productos con errores de formato
                        continue
                        
            else:
                print(f"⚠️  {self.supermercado_nombre} API retornó status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando con {self.supermercado_nombre}: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando respuesta de {self.supermercado_nombre}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado en {self.supermercado_nombre}: {e}")
            
        return productos
