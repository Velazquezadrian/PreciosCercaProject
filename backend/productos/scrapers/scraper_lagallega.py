# Scraper para La Gallega (similar a La Reina)
from .base_scraper import BaseScraper
from typing import List, Dict
import re

class ScraperLaGallega(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://lagallega.com.ar",
            supermercado_nombre="La Gallega"
        )
    
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []
        
        soup = self.hacer_request(self.base_url)
        if not soup:
            return productos
        
        # Buscar productos en la página principal
        # La Gallega tiene estructura similar a La Reina
        textos_productos = soup.find_all(text=re.compile(query, re.IGNORECASE))
        
        for texto in textos_productos:
            try:
                # Buscar contenedor padre
                contenedor = texto.parent
                if not contenedor:
                    continue
                
                # Extraer precio del contenedor
                contenedor_texto = contenedor.get_text()
                precio_match = re.search(r'\$[\d.,]+', contenedor_texto)
                
                if precio_match:
                    precio_texto = precio_match.group()
                    precio = self.limpiar_precio(precio_texto)
                    nombre = self.extraer_nombre_producto(contenedor_texto, precio_texto)
                    
                    if nombre and precio:
                        productos.append({
                            'nombre': nombre.strip(),
                            'precio': precio,
                            'supermercado': self.supermercado_nombre,
                            'url': self.base_url
                        })
                        
            except Exception as e:
                print(f"Error procesando producto La Gallega: {e}")
                continue
                
        return productos
    
    def limpiar_precio(self, precio_texto: str) -> float:
        # Convertir "$1.236,00" a 1236.00
        precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.')
        return float(precio_limpio)
    
    def extraer_nombre_producto(self, texto: str, precio_texto: str) -> str:
        # Extraer nombre antes del precio
        partes = texto.split(precio_texto)
        if len(partes) > 0:
            nombre = partes[0].strip()
            # Limpiar texto extra
            nombre = re.sub(r'OFERTA|DTO \d+%|AGREGAR', '', nombre).strip()
            return nombre
        return ""