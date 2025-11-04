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
        
        # Dividir query en palabras para búsqueda más flexible
        # Ejemplo: "dulce de leche" -> buscar productos que contengan todas las palabras
        palabras = query.lower().split()
        palabras_importantes = [p for p in palabras if p not in ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una']]
        
        # Si después de filtrar no quedan palabras, usar todas
        if not palabras_importantes:
            palabras_importantes = palabras
        
        # Buscar productos que contengan al menos una de las palabras importantes
        # Luego filtrar los que contengan todas
        patron_busqueda = '|'.join(palabras_importantes)
        textos_productos = soup.find_all(text=re.compile(patron_busqueda, re.IGNORECASE))
        
        productos_vistos = set()  # Para evitar duplicados
        
        for texto in textos_productos:
            try:
                # Buscar contenedor padre
                contenedor = texto.parent
                if not contenedor:
                    continue
                
                # Extraer precio del contenedor
                contenedor_texto = contenedor.get_text()
                
                # Verificar que el texto contenga todas las palabras importantes de la búsqueda
                texto_lower = contenedor_texto.lower()
                if not all(palabra in texto_lower for palabra in palabras_importantes):
                    continue
                
                precio_match = re.search(r'\$[\d.,]+', contenedor_texto)
                
                if precio_match:
                    precio_texto = precio_match.group()
                    precio = self.limpiar_precio(precio_texto)
                    nombre = self.extraer_nombre_producto(contenedor_texto, precio_texto)
                    
                    # Buscar imagen en el contenedor
                    imagen_url = None
                    img_tag = contenedor.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', '')
                        if img_src:
                            if img_src.startswith('/'):
                                imagen_url = f"{self.base_url}{img_src}"
                            else:
                                imagen_url = img_src
                    
                    if nombre and precio:
                        # Evitar duplicados usando el nombre como clave
                        producto_key = f"{nombre}_{precio}"
                        if producto_key not in productos_vistos:
                            productos_vistos.add(producto_key)
                            productos.append({
                                'nombre': nombre.strip(),
                                'precio': precio,
                                'supermercado': self.supermercado_nombre,
                                'url': self.base_url,
                                'imagen': imagen_url
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