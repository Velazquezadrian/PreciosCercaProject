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
        
        # Dividir query en palabras para búsqueda más flexible
        # Ejemplo: "dulce de leche" -> buscar productos que contengan todas las palabras importantes
        palabras = query.lower().split()
        # Filtrar palabras comunes que no aportan valor a la búsqueda
        palabras_importantes = [p for p in palabras if p not in ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una']]
        
        # Si después de filtrar no quedan palabras, usar todas
        if not palabras_importantes:
            palabras_importantes = palabras
        
        # Buscar imágenes de productos
        productos_html = soup.find_all("img", {'src': re.compile(r'/Fotos/Articulos/')})

        productos_vistos = set()  # Para evitar duplicados

        for img in productos_html:
            try:
                # Encontrar contenedor padre del producto
                contenedor = img.find_parent()
                if not contenedor:
                    continue

                # Extraer todo el texto del contenedor
                texto = contenedor.get_text()

                # Filtrar solo productos que contengan TODAS las palabras importantes de la búsqueda
                texto_lower = texto.lower()
                if not all(palabra in texto_lower for palabra in palabras_importantes):
                    continue

                # Buscar precio en el texto
                precio_match = re.search(r'\$([\d.,]+)', texto)
                if not precio_match:
                    continue

                precio_texto = precio_match.group()
                precio = self.limpiar_precio(precio_texto)

                # Extraer nombre del producto
                nombre = self.extraer_nombre_producto(texto, precio_texto)
                
                # Extraer URL de la imagen
                imagen_url = None
                img_src = img.get('src', '')
                if img_src:
                    # Si es una URL relativa, hacerla absoluta
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