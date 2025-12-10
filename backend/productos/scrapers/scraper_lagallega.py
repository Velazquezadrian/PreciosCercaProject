from .base_scraper import BaseScraper
from typing import List, Dict
import re
from bs4 import BeautifulSoup
import sys
import os

# Importar cache_manager desde backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from cache_manager import cache_manager

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
    
    def _auto_precargar(self):
        """Precarga automática del catálogo completo de La Gallega"""
        print("")
        print("="*80)
        print("🚀 AUTOPRECARGA: Catálogo de La Gallega vacío, iniciando carga completa...")
        print("="*80)
        print("⚠️  Este proceso puede tardar 15-20 minutos (136 categorías)")
        print("⚠️  Solo se ejecutará una vez, luego las búsquedas serán instantáneas")
        print("")
        
        todas_las_categorias = self.categorias
        print(f"📊 Procesando {len(todas_las_categorias)} categorías completas...")
        print("")
        
        total_productos = 0
        from time import sleep
        
        for i, categoria in enumerate(todas_las_categorias, 1):
            try:
                print(f"[{i}/{len(todas_las_categorias)}] '{categoria}'...", end=" ", flush=True)
                
                url_categoria = f"{self.base_url}/productosnl.asp?nl={categoria}&TM=cx"
                soup = self.hacer_request(url_categoria)
                
                if not soup:
                    print("❌ Sin respuesta")
                    continue
                
                productos_html = soup.find_all('li', {'class': 'cuadProd'})
                productos_guardados = 0
                
                for prod_li in productos_html:
                    try:
                        nombre_elem = prod_li.find('span', {'class': 'prodNombre'})
                        if not nombre_elem or not nombre_elem.get_text(strip=True):
                            img_fallback = prod_li.find('img')
                            if img_fallback and img_fallback.get('alt'):
                                alt = img_fallback.get('alt', '')
                                nombre = alt.split(' - ', 1)[1] if ' - ' in alt else alt
                            else:
                                continue
                        else:
                            nombre = nombre_elem.get_text(strip=True)
                        
                        if not nombre or nombre in cache_manager.cache['productos']['lagallega']:
                            continue
                        
                        precio_match = re.search(r'\$\s*([\d.,]+)', prod_li.get_text())
                        if not precio_match:
                            continue
                        precio = self.limpiar_precio(precio_match.group(0))
                        
                        img_elem = prod_li.find('img')
                        imagen_url = None
                        if img_elem and img_elem.get('src'):
                            img_src = img_elem.get('src')
                            imagen_url = img_src if img_src.startswith('http') else f"{self.base_url}{img_src if img_src.startswith('/') else '/' + img_src}"
                        
                        link = prod_li.find('a', href=True)
                        producto_url = self.base_url
                        if link and link.get('href'):
                            href = link.get('href')
                            producto_url = href if href.startswith('http') else f"{self.base_url}{href if href.startswith('/') else '/' + href}"
                        
                        cache_manager.agregar_producto(
                            supermercado='lagallega',
                            nombre=nombre,
                            categoria=categoria,
                            precio=precio,
                            url=producto_url,
                            imagen_url=imagen_url
                        )
                        
                        productos_guardados += 1
                        total_productos += 1
                    except:
                        continue
                
                print(f"✅ {productos_guardados} productos")
                
                if i % 10 == 0:
                    cache_manager.guardar_cache()
                
                sleep(0.5)
                
            except:
                print(f"❌ Error")
                continue
        
        cache_manager.guardar_cache()
        print("")
        print("="*80)
        print(f"✅ AUTOPRECARGA COMPLETADA: {total_productos} productos guardados")
        print("="*80)
        print("")
    
    def buscar_productos(self, query: str) -> List[Dict]:
        """
        Buscar productos en La Gallega usando caché inteligente.
        
        Estrategia:
        1. PRIMERO busca en caché local (instantáneo)
        2. Si no hay suficientes resultados, busca en web y actualiza caché
        3. Las imágenes se descargan y optimizan localmente
        """
        # PASO 1: Buscar en caché
        print(f"🔍 Buscando '{query}' en La Gallega...")
        productos_cache = cache_manager.buscar_producto('lagallega', query)
        
        print(f"💾 Encontrados {len(productos_cache)} productos en caché")
        
        # Si el caché tiene un catálogo completo (>500 productos totales), confiar en él
        total_en_cache = len(cache_manager.cache['productos'].get('lagallega', {}))
        print(f"💾 Total productos en caché de La Gallega: {total_en_cache}")
        
        # Si el caché está vacío o muy pequeño, hacer autoprecarga
        if total_en_cache < 100:
            print(f"⚠️  Caché insuficiente ({total_en_cache} productos), iniciando autoprecarga...")
            self._auto_precargar()
            # Volver a buscar después de precargar
            productos_cache = cache_manager.buscar_producto('lagallega', query)
            total_en_cache = len(cache_manager.cache['productos'].get('lagallega', {}))
        
        # ESTRATEGIA: Si hay pocos resultados en caché, buscar también en web
        # Umbral: menos de 30 productos → complementar con scraping web
        if total_en_cache > 500 and len(productos_cache) >= 30:
            # Caché completo precargado con suficientes resultados, usar SOLO caché (búsqueda instantánea)
            print(f"⚡ Usando caché completo precargado (búsqueda instantánea)")
            return self._formatear_productos_cache(productos_cache)
        elif total_en_cache > 500:
            print(f"⚠️  Solo {len(productos_cache)} resultados en caché, complementando con búsqueda web...")
        
        # Si no hay caché completo, buscar en web (modo antiguo)
        print(f"🌐 Caché incompleto, buscando en web...")
        
        # PASO 2: Buscar en web para complementar
        print(f"🌐 Buscando más productos en web...")
        productos = []
        productos_vistos = set()
        
        # Limpiar query y separar palabras
        palabras_query = set(query.lower().split())
        
        # Remover stopwords comunes
        stopwords = {'de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'y', 'con', 'sin'}
        palabras_query = palabras_query - stopwords
        
        if not palabras_query:
            palabras_query = set(query.lower().split())
        
        print(f"   Palabras clave: {palabras_query}")
        print(f"   Total categorías disponibles: {len(self.categorias)}")
        
        # Usar TODAS las categorías para búsqueda completa
        # La paginación en la API evita timeout al cliente
        categorias_a_buscar = self.categorias
        
        print(f"   Buscando en {len(categorias_a_buscar)} categorías")
        
        for i, nl_code in enumerate(categorias_a_buscar, 1):
            
            try:
                url = f"{self.base_url}/productosnl.asp?nl={nl_code}"
                soup = self.hacer_request(url)
                
                if not soup:
                    continue
                
                # Buscar productos en <li class="cuadProd">
                productos_li = soup.find_all('li', class_='cuadProd')
                
                for prod_li in productos_li:
                    try:
                        # Extraer nombre PRIMERO
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
                        
                        # Verificar si el NOMBRE contiene TODAS las palabras de búsqueda
                        # Patrón: *palabra1*palabra2*palabra3* (palabras pueden estar separadas)
                        # "pan" → acepta "pan lactal", "bizcochos de pan", "pan x kg"
                        # "dulce de leche" → acepta "dulce de leche", "dulce leche condensada"
                        nombre_lower = ' ' + nombre.lower() + ' '
                        
                        # Verificar que TODAS las palabras estén presentes (en cualquier orden)
                        tiene_todas = True
                        for palabra in palabras_query:
                            # Buscar palabra con espacios antes (evita "emPANada")
                            if ' ' + palabra not in nombre_lower:
                                tiene_todas = False
                                break
                        
                        if not tiene_todas:
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
                        
                        producto_dict = {
                            'nombre': nombre,
                            'precio': precio,
                            'supermercado': self.supermercado_nombre,
                            'imagen': imagen_url,
                            'url': producto_url,
                            'categoria': nl_code
                        }
                        
                        productos.append(producto_dict)
                        
                        # Guardar en caché (con descarga optimizada de imagen)
                        cache_manager.agregar_producto(
                            supermercado='lagallega',
                            nombre=nombre,
                            categoria=nl_code,
                            precio=precio,
                            url=producto_url,
                            imagen_url=imagen_url
                        )
                    
                    except Exception as e:
                        # Error procesando producto individual, continuar con el siguiente
                        continue
                
                print(f"  📂 Categoría {i}/{len(categorias_a_buscar)}: {len(productos_li)} productos, {len(productos)} relevantes acumulados")
            
            except Exception as e:
                print(f"  ⚠️ Error en categoría {nl_code}: {str(e)[:100]}")
                continue
        
        # Guardar caché después de scraping
        cache_manager.guardar_cache()
        
        print(f"✅ Scraping completado: {len(productos)} productos nuevos")
        
        # COMBINAR productos del caché con los nuevos del scraping
        # para evitar duplicados
        if productos_cache:
            print(f"   Combinando con {len(productos_cache)} del caché...")
            nombres_scraping = {p['nombre'].lower() for p in productos}
            
            for prod_cache in productos_cache:
                # Solo agregar si no está ya en los resultados del scraping
                if prod_cache['nombre'].lower() not in nombres_scraping:
                    productos.append({
                        'nombre': prod_cache['nombre'],
                        'precio': prod_cache['precio'],
                        'supermercado': self.supermercado_nombre,
                        'imagen': prod_cache.get('imagen_url'),
                        'url': prod_cache['url']
                    })
        
        print(f"✅ Total productos retornados: {len(productos)}\n")
        
        return productos
    
    def _formatear_productos_cache(self, productos_cache):
        """Convierte productos del caché al formato esperado por la API"""
        productos_formateados = []
        
        for prod in productos_cache:
            # Usar directamente la URL original de la imagen
            # Android + Glide se encargan de descargar y cachear
            
            productos_formateados.append({
                'nombre': prod['nombre'],
                'precio': prod['precio'],
                'supermercado': self.supermercado_nombre,
                'imagen': prod.get('imagen_url'),  # URL directa
                'url': prod['url']
            })
        
        return productos_formateados
    
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