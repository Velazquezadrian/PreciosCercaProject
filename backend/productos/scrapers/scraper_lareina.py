# Scraper específico para supermercado La Reina
from .base_scraper import BaseScraper
from typing import List, Dict
import re

class ScraperLaReina(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://www.lareinaonline.com.ar",
            supermercado_nombre="La Reina"
        )
        self.categorias = self._obtener_categorias()
    
    def _obtener_categorias(self) -> List[str]:
        """Extrae todas las categorías disponibles desde la página principal"""
        try:
            soup = self.hacer_request(self.base_url)
            if not soup:
                return []
            
            # Buscar todos los links a productosnl.asp
            links = soup.find_all('a', href=re.compile(r'productosnl\.asp\?nl='))
            categorias = []
            
            for link in links:
                href = link.get('href', '')
                # Extraer código de categoría: productosnl.asp?nl=01010100&TM=cx
                match = re.search(r'nl=(\d{8})', href)
                if match:
                    categorias.append(match.group(1))
            
            return list(set(categorias))  # Eliminar duplicados
        except:
            # Si falla, usar categorías hardcodeadas básicas
            return ['01010100', '01020100', '01030100', '01040100']
        
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []
        productos_vistos = set()
        
        # Palabras importantes del query (filtrar stopwords)
        palabras = query.lower().split()
        palabras_importantes = [p for p in palabras if p not in ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'en']]
        if not palabras_importantes:
            palabras_importantes = palabras
        
        # Buscar en máximo 30 categorías para evitar timeouts
        max_categorias = min(30, len(self.categorias))
        categorias_a_buscar = self.categorias[:max_categorias]
        
        # Buscar en múltiples categorías
        for i, categoria in enumerate(categorias_a_buscar):
            # Stop early si ya tenemos suficientes productos
            if len(productos) >= 50:
                break
                
            url_categoria = f"{self.base_url}/productosnl.asp?nl={categoria}&TM=cx"
            
            try:
                soup = self.hacer_request(url_categoria)
                if not soup:
                    continue
                
                # Buscar productos en <li class="cuadProd">
                productos_html = soup.find_all('li', {'class': 'cuadProd'})
                
                for producto_li in productos_html:
                    try:
                        texto_completo = producto_li.get_text()
                        texto_lower = texto_completo.lower()
                        
                        # Filtrar por query (debe contener todas las palabras importantes)
                        if not all(palabra in texto_lower for palabra in palabras_importantes):
                            continue
                        
                        # Buscar precio
                        precio_match = re.search(r'\$[\d.,]+', texto_completo)
                        if not precio_match:
                            continue
                        
                        precio_texto = precio_match.group()
                        precio = self.limpiar_precio(precio_texto)
                        
                        # Extraer nombre (todo el texto antes del precio)
                        nombre = texto_completo.split(precio_texto)[0].strip()
                        nombre = re.sub(r'\s+', ' ', nombre)  # Limpiar espacios múltiples
                        
                        # Buscar imagen
                        img = producto_li.find('img', {'src': re.compile(r'.*Articulos.*', re.I)})
                        imagen_url = None
                        if img:
                            img_src = img.get('src', '')
                            if img_src:
                                if img_src.startswith('http'):
                                    imagen_url = img_src
                                elif img_src.startswith('/'):
                                    imagen_url = f"{self.base_url}{img_src}"
                                else:
                                    imagen_url = f"{self.base_url}/{img_src}"
                        
                        if nombre and precio:
                            producto_key = f"{nombre}_{precio}"
                            if producto_key not in productos_vistos:
                                productos_vistos.add(producto_key)
                                productos.append({
                                    'nombre': nombre.title(),
                                    'precio': precio,
                                    'supermercado': self.supermercado_nombre,
                                    'url': url_categoria,
                                    'imagen': imagen_url
                                })
                                
                                # Limitar a 50 productos
                                if len(productos) >= 50:
                                    return productos
                    
                    except Exception as e:
                        continue
            
            except Exception as e:
                # Si una categoría falla, continuar con la siguiente
                print(f"Error en categoría {categoria}: {e}")
                continue
        
        return productos
    
    def limpiar_precio(self, precio_texto: str) -> float:
        # Convertir "$2.779,00" a 2779.00
        precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.')
        return float(precio_limpio)