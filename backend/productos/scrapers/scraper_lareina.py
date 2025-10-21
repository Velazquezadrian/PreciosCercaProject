# Scraper específico para supermercado La Reina
from .base_scraper import BaseScraper
from typing import List, Dict
import re

class ScraperLaReina(BaseScraper):
    def __init__(self):
        # Inicializar con URL base y nombre del supermercado
        super().__init__(
            base_url="https://www.lareinaonline.com.ar",
            supermercado_nombre="La Reina"
        )
        
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []

        soup = self.hacer_request(self.base_url)
        if not soup:
            return productos
        
        # Buscar imágenes de productos
        productos_html = soup.find_all("img", {'src': re.compile(r'/Fotos/Articulos/')})

        for img in productos_html:
            try:
                # Encontrar contenedor padre del producto
                contenedor = img.find_parent()
                if not contenedor:
                    continue

                # Extraer todo el texto del contenedor
                texto = contenedor.get_text()

                # Filtrar solo productos que contengan la búsqueda
                if query.lower() not in texto.lower():
                    continue

                # Buscar precio en el texto
                precio_match = re.search(r'\$([\d.,]+)', texto)
                if not precio_match:
                    continue

                precio_texto = precio_match.group()
                precio = self.limpiar_precio(precio_texto)

                # Extraer nombre del producto
                nombre = self.extraer_nombre_producto(texto, precio_texto)

                if nombre and precio:
                    productos.append({
                        'nombre': nombre.strip(),
                        'precio': precio,
                        'supermercado': self.supermercado_nombre,
                        'url': self.base_url
                    })
            
            except Exception as e:
                print(f"Error al procesar un producto: {e}")
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
            # Limpiar texto extra como OFERTA, DTO, etc.
            nombre = re.sub(r'OFERTA|DTO \d+%|AGREGAR', '', nombre).strip()
            return nombre
        return ""