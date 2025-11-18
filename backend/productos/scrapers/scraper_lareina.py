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
        # Categorías completas descubiertas mediante mapeo sistemático
        self.categorias = [
            # Nivel 1: Categorías principales (9 categorías)
            '01000000', '02000000', '03000000', '04000000', '05000000',
            '06000000', '07000000', '08000000', '09000000',
            # Nivel 2: Subcategorías (53 categorías)
            '01010000', '01020000', '01030000', '01040000', '01050000',
            '01060000', '01070000', '01080000', '01090000', '02010000',
            '02020000', '02030000', '02040000', '02050000', '02060000',
            '02070000', '02080000', '02090000', '03010000', '03020000',
            '03030000', '03040000', '03060000', '04010000', '04020000',
            '04030000', '04040000', '04050000', '05010000', '05020000',
            '06010000', '06020000', '06030000', '06040000', '06050000',
            '06060000', '06070000', '07010000', '07020000', '07030000',
            '07040000', '07050000', '07060000', '07070000', '07080000',
            '07090000', '08010000', '08030000', '08040000', '08050000',
            '08060000', '08070000', '08080000',
            # Nivel 3: Sub-subcategorías (150 categorías)
            '01010100', '01010200', '01010300', '01010400', '01010500',
            '01020100', '01020200', '01020300', '01020400', '01030100',
            '01030200', '01040100', '01040200', '01040300', '01040400',
            '01040500', '01050100', '01050200', '01060100', '01060200',
            '01060300', '01060400', '01070100', '01070200', '01070300',
            '01070400', '01070500', '01070600', '01070700', '01080100',
            '01080200', '01080300', '01080400', '01080500', '01080600',
            '01080700', '01090200', '01090300', '01090400', '01090500',
            '01090600', '02010100', '02010200', '02010300', '02020100',
            '02020200', '02020300', '02020400', '02030100', '02030200',
            '02040100', '02040200', '03010100', '03010200', '03010300',
            '03010400', '03010500', '03020100', '03020200', '03020400',
            '03020500', '03030100', '03030200', '03030300', '03030400',
            '03030500', '03030600', '03030700', '03040100', '03040200',
            '03040300', '03040400', '03060100', '03060200', '03060300',
            '03060400', '03060500', '03060600', '03060700', '03060800',
            '04010100', '04020100', '04020200', '04020300', '04030100',
            '04030200', '05010100', '05010200', '05010300', '06010200',
            '06010300', '06010500', '06010600', '06020200', '06020300',
            '06020400', '06020500', '06020600', '06020700', '06020800',
            '06020900', '06030100', '06030200', '06030300', '06030400',
            '06040100', '06040200', '06040300', '06050100', '06050200',
            '06050400', '06060100', '06060200', '06070100', '06070200',
            '06070300', '07010100', '07010200', '07010300', '07010400',
            '07010500', '07010600', '07010700', '07010800', '07010900',
            '07020100', '07020200', '07020300', '07030100', '07030200',
            '07030300', '07030400', '07030500', '07040100', '07040200',
            '07040300', '07050100', '07050200', '07050300', '07050400',
            '07050500', '07070100', '07070200', '07070300', '07080100',
            '07080200', '07080300', '07080400', '07090100', '07090200',
        ]
        # Total: 212 categorías (9 nivel 1 + 53 nivel 2 + 150 nivel 3)
        
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []
        productos_vistos = set()
        
        # Palabras importantes del query (filtrar stopwords)
        palabras = query.lower().split()
        palabras_importantes = [p for p in palabras if p not in ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'en']]
        if not palabras_importantes:
            palabras_importantes = palabras
        
        # Buscar en todas las categorías con detención temprana
        # (212 categorías totales, detención al encontrar 50 productos)
        categorias_a_buscar = self.categorias
        
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