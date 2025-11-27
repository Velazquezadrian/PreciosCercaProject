# Scraper específico para supermercado La Reina
from .base_scraper import BaseScraper
from typing import List, Dict
import re
import sys
import os

# Importar cache_manager desde backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from cache_manager import cache_manager

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
        
    def _auto_precargar(self):
        """Precarga automática del catálogo completo de La Reina"""
        print("")
        print("="*80)
        print("🚀 AUTOPRECARGA: Catálogo de La Reina vacío, iniciando carga completa...")
        print("="*80)
        print("⚠️  Este proceso puede tardar 8-12 minutos")
        print("⚠️  Solo se ejecutará una vez, luego las búsquedas serán instantáneas")
        print("")
        
        # Usar TODAS las 212 categorías para precarga completa
        todas_categorias = self.categorias
        
        print(f"📊 Procesando {len(todas_categorias)} categorías (niveles 1, 2 y 3)...")
        print("")
        
        total_productos = 0
        productos_vistos = set()
        from time import sleep
        
        for i, cat in enumerate(todas_categorias, 1):
            try:
                print(f"[{i}/{len(todas_categorias)}] '{cat}'...", end=" ", flush=True)
                
                url_categoria = f"{self.base_url}/productosnl.asp?nl={cat}&TM=cx"
                soup = self.hacer_request(url_categoria)
                
                if not soup:
                    print("❌ Sin respuesta")
                    continue
                
                productos_html = soup.find_all('li', {'class': 'cuadProd'})
                productos_guardados = 0
                
                for prod_li in productos_html:
                    try:
                        texto_completo = prod_li.get_text()
                        
                        # Buscar precio
                        precio_match = re.search(r'\$[\d.,]+', texto_completo)
                        if not precio_match:
                            continue
                        
                        precio_texto = precio_match.group()
                        precio = self.limpiar_precio(precio_texto)
                        
                        # Extraer nombre (todo el texto antes del precio)
                        nombre = texto_completo.split(precio_texto)[0].strip()
                        nombre = re.sub(r'\s+', ' ', nombre)  # Limpiar espacios múltiples
                        
                        if not nombre:
                            continue
                        
                        # Evitar duplicados por nombre
                        producto_key = f"{nombre}_{precio}"
                        if producto_key in productos_vistos:
                            continue
                        productos_vistos.add(producto_key)
                        
                        # Buscar imagen
                        img = prod_li.find('img', {'src': re.compile(r'.*Articulos.*', re.I)})
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
                        
                        cache_manager.agregar_producto(
                            supermercado='lareina',
                            nombre=nombre.title(),
                            categoria=cat,
                            precio=precio,
                            url=url_categoria,
                            imagen_url=imagen_url
                        )
                        
                        productos_guardados += 1
                        total_productos += 1
                    except:
                        continue
                
                print(f"✅ {productos_guardados} productos")
                
                # Guardar cada 20 categorías en lugar de cada 3
                if i % 20 == 0:
                    cache_manager.guardar_cache()
                    print(f"   💾 Caché guardado ({total_productos} productos totales)")
                
                sleep(0.3)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        cache_manager.guardar_cache()
        print("")
        print("="*80)
        print(f"✅ AUTOPRECARGA COMPLETADA: {total_productos} productos guardados")
        print("="*80)
        print("")
    
    def buscar_productos(self, query: str) -> List[Dict]:
        # PASO 1: Buscar en caché
        print(f"[La Reina] Buscando '{query}'...")
        productos_cache = cache_manager.buscar_producto('lareina', query)
        print(f"💾 {len(productos_cache)} productos en caché")
        
        # Si tenemos el catálogo completo precargado, usar solo caché
        total_en_cache = len(cache_manager.cache['productos'].get('lareina', {}))
        
        # Si el caché está vacío o muy pequeño, hacer autoprecarga
        if total_en_cache < 100:
            print(f"⚠️  Caché insuficiente ({total_en_cache} productos), iniciando autoprecarga...")
            self._auto_precargar()
            # Volver a buscar después de precargar
            productos_cache = cache_manager.buscar_producto('lareina', query)
            total_en_cache = len(cache_manager.cache['productos'].get('lareina', {}))
        
        if total_en_cache > 500:
            print(f"⚡ Usando caché completo precargado ({total_en_cache} productos totales) - búsqueda instantánea")
            return self._formatear_productos_cache(productos_cache)
        
        if len(productos_cache) >= 20:
            print(f"⚡ Suficientes en caché, retornando")
            return self._formatear_productos_cache(productos_cache)
        
        # PASO 2: Buscar en web
        print(f"🌐 Buscando más en web...")
        productos = []
        productos_vistos = set()
        
        # OPTIMIZACIÓN: Buscar solo en las 9 categorías principales (nivel 1)
        categorias_principales = [
            '01000000', '02000000', '03000000', '04000000', '05000000',
            '06000000', '07000000', '08000000', '09000000'
        ]
        
        # Buscar en categorías principales solamente
        for i, categoria in enumerate(categorias_principales):
                
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
                                
                                # Guardar en caché
                                cache_manager.agregar_producto(
                                    supermercado='lareina',
                                    nombre=nombre.title(),
                                    categoria=categoria,
                                    precio=precio,
                                    url=url_categoria,
                                    imagen_url=imagen_url
                                )
                    
                    except Exception as e:
                        continue
            
            except Exception as e:
                # Si una categoría falla, continuar con la siguiente
                print(f"Error en categoría {categoria}: {e}")
                continue
        
        # Guardar caché
        cache_manager.guardar_cache()
        
        print(f"✅ Scraping: {len(productos)} productos nuevos")
        
        # COMBINAR con caché
        if productos_cache:
            print(f"   Combinando con {len(productos_cache)} del caché...")
            nombres_scraping = {p['nombre'].lower() for p in productos}
            
            for prod_cache in productos_cache:
                if prod_cache['nombre'].lower() not in nombres_scraping:
                    productos.append({
                        'nombre': prod_cache['nombre'],
                        'precio': prod_cache['precio'],
                        'supermercado': self.supermercado_nombre,
                        'imagen': prod_cache.get('imagen_url'),
                        'url': prod_cache['url']
                    })
        
        print(f"✅ Total retornados: {len(productos)}")
        return productos
    
    def _formatear_productos_cache(self, productos_cache):
        """Convierte productos del caché al formato esperado"""
        return [{
            'nombre': p['nombre'],
            'precio': p['precio'],
            'supermercado': self.supermercado_nombre,
            'imagen': p.get('imagen_url'),
            'url': p['url']
        } for p in productos_cache]
    
    def limpiar_precio(self, precio_texto: str) -> float:
        # Convertir "$2.779,00" a 2779.00
        precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.')
        return float(precio_limpio)