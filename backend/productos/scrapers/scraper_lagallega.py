from .base_scraper import BaseScraper
from typing import List, Dict
import re
from bs4 import BeautifulSoup

class ScraperLaGallega(BaseScraper):
    """
    Scraper para La Gallega Online
    
    La Gallega usa estructura similar a La Reina:
    - Categorías con parámetro nl=XXXXXXXX
    - Productos en <li class="cuadProd">
    - Carga dinámica con JavaScript (pero funciona con requests si sabemos las categorías)
    """
    
    def __init__(self):
        super().__init__(
            base_url="https://www.lagallega.com.ar",
            supermercado_nombre="La Gallega"
        )
        
        # Categorías principales hardcodeadas (extraídas manualmente del menú)
        # Estas se obtuvieron navegando el sitio y guardando los códigos nl=
        self.categorias = self._obtener_categorias()
    
    def _obtener_categorias(self) -> List[str]:
        """
        Obtener categorías de La Gallega.
        
        Por ahora usamos categorías hardcodeadas porque el sitio 
        carga el menú con JavaScript.
        
        TODO: Implementar extracción dinámica con Selenium si es necesario
        """
        
        # Intentar obtener dinámicamente primero
        categorias_dinamicas = self._obtener_categorias_dinamicas()
        if categorias_dinamicas:
            print(f"✅ Categorías dinámicas obtenidas: {len(categorias_dinamicas)}")
            return categorias_dinamicas
        
        # Fallback a categorías conocidas (verificadas manualmente)
        print("⚠️ Usando categorías hardcodeadas de La Gallega")
        
        # Categorías válidas verificadas el 18/11/2025
        # Total: 136 categorías (20 nivel 1 + 116 nivel 2)
        # Incluye categorías generales (8 dígitos) y subcategorías específicas (11 dígitos)
        categorias_conocidas = [
            "02000000", "03000000", "04000000", "05000000", "06000000", 
            "07000000", "08000000", "09000000", "10000000", "11000000",
            "12000000", "13000000", "14000000", "15000000", "16000000", 
            "17000000", "18000000", "19000000", "20000000", "21000000",
            "02000000000", "03000000000", "03010000000", "03020000000", "03030000000",
            "03040000000", "03050000000", "03060000000", "03070000000", "03080000000",
            "03090000000", "04000000000", "04010000000", "04020000000", "05000000000",
            "05010000000", "05020000000", "05030000000", "05040000000", "05050000000",
            "05060000000", "05070000000", "06000000000", "06010000000", "06020000000",
            "06030000000", "06040000000", "06050000000", "06060000000", "06070000000",
            "07000000000", "07010000000", "07020000000", "07030000000", "07040000000",
            "07050000000", "07060000000", "07070000000", "07080000000", "07090000000",
            "08000000000", "08010000000", "08020000000", "08030000000", "08040000000",
            "08050000000", "08060000000", "08070000000", "08080000000", "09000000000",
            "10000000000", "11000000000", "12000000000", "13000000000", "13010000000",
            "13020000000", "13030000000", "13040000000", "13050000000", "13060000000",
            "13070000000", "14000000000", "14010000000", "14020000000", "14030000000",
            "14040000000", "14050000000", "14060000000", "14070000000", "14080000000",
            "15000000000", "15010000000", "15020000000", "15030000000", "15040000000",
            "15060000000", "15070000000", "15080000000", "15090000000", "16000000000",
            "16010000000", "16020000000", "16030000000", "16040000000", "16060000000",
            "16070000000", "16080000000", "16090000000", "17000000000", "17010000000",
            "17020000000", "17030000000", "17040000000", "17050000000", "17060000000",
            "17070000000", "17080000000", "17090000000", "18000000000", "18010000000",
            "18020000000", "18030000000", "19000000000", "19010000000", "19020000000",
            "20000000000", "20010000000", "20020000000", "20030000000", "20040000000",
            "20050000000", "20060000000", "20070000000", "20080000000", "20090000000",
            "21000000000",
        ]
        
        return categorias_conocidas
    
    def _obtener_categorias_dinamicas(self) -> List[str]:
        """
        Intentar obtener categorías dinámicamente del menú.
        
        Returns:
            Lista de códigos nl= o lista vacía si falla
        """
        try:
            # Intentar cargar el menú AJAX
            soup = self.hacer_request(f"{self.base_url}/M2-Menu.asp")
            
            if soup:
                # Buscar todos los enlaces con nl=
                links = soup.find_all('a', href=re.compile(r'nl=(\d{8})'))
                
                categorias = []
                for link in links:
                    href = link.get('href', '')
                    match = re.search(r'nl=(\d{8})', href)
                    if match:
                        nl_code = match.group(1)
                        if nl_code not in categorias:
                            categorias.append(nl_code)
                
                if categorias:
                    return categorias[:30]  # Limitar a 30 para performance
            
            # También buscar en la página principal
            soup2 = self.hacer_request(self.base_url)
            if soup2:
                # Buscar códigos nl= en el HTML completo
                html_text = str(soup2)
                nl_matches = re.findall(r'nl=(\d{8})', html_text)
                if nl_matches:
                    categorias_unicas = list(set(nl_matches))
                    return categorias_unicas[:30]
        
        except Exception as e:
            print(f"⚠️ Error obteniendo categorías dinámicas: {e}")
        
        return []
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Buscar productos en La Gallega.
        
        Estrategia:
        1. Busca en todas las categorías conocidas
        2. Filtra productos que contengan las palabras de búsqueda
        3. Extrae nombre, precio, imagen de cada producto
        4. Retorna lista de hasta 50 productos
        """
        productos = []
        productos_vistos = set()
        
        # Limpiar query y separar palabras
        palabras_query = set(query.lower().split())
        
        # Remover stopwords comunes
        stopwords = {'de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'y', 'con', 'sin'}
        palabras_query = palabras_query - stopwords
        
        if not palabras_query:
            palabras_query = set(query.lower().split())
        
        print(f"🔍 Buscando '{query}' en La Gallega (palabras clave: {palabras_query})")
        print(f"   Total categorías disponibles: {len(self.categorias)}")
        
        # Buscar en TODAS las categorías disponibles (136 total)
        # Pero detener cuando tengamos suficientes productos relevantes
        categorias_a_buscar = self.categorias
        print(f"   Buscando en hasta {len(categorias_a_buscar)} categorías (detención temprana al encontrar 50 productos)")
        
        for i, nl_code in enumerate(categorias_a_buscar, 1):
            if len(productos) >= 50:
                print(f"⚠️ Límite de 50 productos alcanzado, deteniendo búsqueda")
                break
            
            try:
                url = f"{self.base_url}/productosnl.asp?nl={nl_code}"
                soup = self.hacer_request(url)
                
                if not soup:
                    continue
                
                # Buscar productos en <li class="cuadProd">
                productos_li = soup.find_all('li', class_='cuadProd')
                
                for prod_li in productos_li:
                    try:
                        # Obtener texto completo del producto
                        texto_producto = prod_li.get_text().lower()
                        
                        # Verificar si contiene todas las palabras de búsqueda
                        palabras_encontradas = set()
                        for palabra in palabras_query:
                            if palabra in texto_producto:
                                palabras_encontradas.add(palabra)
                        
                        # Debe contener todas las palabras importantes
                        if not palabras_encontradas.issuperset(palabras_query):
                            continue
                        
                        # Extraer nombre
                        # La Gallega usa <div class="desc"> para el nombre
                        nombre_elem = prod_li.find('div', class_='desc')
                        
                        if not nombre_elem:
                            # Fallback: buscar en alt de imagen o enlace
                            img_fallback = prod_li.find('img')
                            if img_fallback and img_fallback.get('alt'):
                                # El alt tiene formato "codigo - nombre"
                                alt = img_fallback.get('alt', '')
                                if ' - ' in alt:
                                    nombre = alt.split(' - ', 1)[1]  # Tomar la parte después del código
                                else:
                                    nombre = alt
                            else:
                                # Usar primer texto largo
                                textos = [t.strip() for t in prod_li.stripped_strings if len(t.strip()) > 5 and '$' not in t and 'Agregar' not in t]
                                nombre = textos[0] if textos else None
                        else:
                            nombre = nombre_elem.get_text(strip=True)
                        
                        if not nombre:
                            continue
                        
                        # Extraer precio
                        precio_match = re.search(r'\$\s*([\d.,]+)', prod_li.get_text())
                        if not precio_match:
                            continue
                        
                        try:
                            precio = self.limpiar_precio(precio_match.group(0))
                        except:
                            continue
                        
                        # Extraer imagen (buscar cada vez, no reutilizar variable)
                        img_elem = prod_li.find('img')
                        imagen_url = None
                        if img_elem:
                            img_src = img_elem.get('src', '')
                            if img_src:
                                # Construir URL completa
                                if img_src.startswith('http'):
                                    imagen_url = img_src
                                elif img_src.startswith('/'):
                                    imagen_url = f"{self.base_url}{img_src}"
                                else:
                                    imagen_url = f"{self.base_url}/{img_src}"
                        
                        # Extraer URL del producto
                        link = prod_li.find('a', href=True)
                        producto_url = self.base_url
                        if link:
                            href = link.get('href', '')
                            if href.startswith('http'):
                                producto_url = href
                            elif href.startswith('/'):
                                producto_url = f"{self.base_url}{href}"
                            else:
                                producto_url = f"{self.base_url}/{href}"
                        
                        # Evitar duplicados
                        producto_key = f"{nombre}_{precio}"
                        if producto_key in productos_vistos:
                            continue
                        
                        productos_vistos.add(producto_key)
                        
                        productos.append({
                            'nombre': nombre,
                            'precio': precio,
                            'supermercado': self.supermercado_nombre,
                            'imagen': imagen_url,
                            'url': producto_url
                        })
                        
                        if len(productos) >= 50:
                            break
                    
                    except Exception as e:
                        # Error procesando producto individual, continuar con el siguiente
                        continue
                
                print(f"  📂 Categoría {i}/{len(categorias_a_buscar)}: {len(productos_li)} productos, {len(productos)} relevantes acumulados")
            
            except Exception as e:
                print(f"  ⚠️ Error en categoría {nl_code}: {str(e)[:100]}")
                continue
        
        print(f"✅ Búsqueda completada: {len(productos)} productos encontrados\n")
        
        return productos
    
    def limpiar_precio(self, precio_texto: str) -> float:
        """
        Convertir "$1.236,00" a 1236.00
        
        Args:
            precio_texto: String con formato "$1.236,00" o "$1236.00"
        
        Returns:
            Float con el precio limpio
        """
        # Remover símbolo $ y espacios
        precio_limpio = precio_texto.replace('$', '').strip()
        
        # Remover puntos de miles y convertir coma decimal a punto
        precio_limpio = precio_limpio.replace('.', '').replace(',', '.')
        
        return float(precio_limpio)