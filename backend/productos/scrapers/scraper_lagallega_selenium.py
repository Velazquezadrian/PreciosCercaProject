#!/usr/bin/env python3
"""
Scraper mejorado para La Gallega usando undetected-chromedriver
para manejar contenido dinámico con JavaScript de forma más robusta
"""

from .base_scraper import BaseScraper
from typing import List, Dict
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class ScraperLaGallegaSelenium(BaseScraper):
    def __init__(self):
        super().__init__(
            base_url="https://lagallega.com.ar",
            supermercado_nombre="La Gallega"
        )
        self.driver = None
        
    def _init_driver(self):
        """Inicializar el driver de Chrome usando undetected-chromedriver"""
        if self.driver is None:
            try:
                options = uc.ChromeOptions()
                options.add_argument('--headless=new')  # Modo headless mejorado
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-blink-features=AutomationControlled')
                
                self.driver = uc.Chrome(options=options, version_main=None)
                print("✅ Chrome driver (undetected) inicializado correctamente")
            except Exception as e:
                print(f"❌ Error inicializando Chrome driver: {e}")
                self.driver = None
    
    def _close_driver(self):
        """Cerrar el driver si está activo"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def buscar_productos(self, query: str) -> List[Dict]:
        productos = []
        
        try:
            # Inicializar driver si no existe
            self._init_driver()
            if not self.driver:
                print("⚠️ No se pudo inicializar el driver de Chrome")
                return productos
            
            # Dividir query en palabras para búsqueda más flexible
            palabras = query.lower().split()
            palabras_importantes = [p for p in palabras if p not in ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una']]
            
            if not palabras_importantes:
                palabras_importantes = palabras
            
            print(f"🔍 Buscando '{query}' en La Gallega (palabras clave: {', '.join(palabras_importantes)})")
            
            # Cargar la página principal
            self.driver.get(self.base_url)
            
            # Esperar a que se cargue el contenido dinámico (el div fArticulos)
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "fArticulos"))
                )
                # Esperar un poco más para que el contenido AJAX termine de cargar
                time.sleep(3)
                
                # Hacer scroll para cargar más productos
                print("  📜 Haciendo scroll para cargar más productos...")
                for i in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                
                print("  ⏳ Esperando carga adicional...")
                time.sleep(2)
                
                # Verificar si hay contenido cargado
                articulos_div = self.driver.find_element(By.ID, "fArticulos")
                if articulos_div.text.strip():
                    print(f"  ✅ Contenido cargado ({len(articulos_div.text)} caracteres)")
                else:
                    print("  ⚠️ Div fArticulos está vacío")
                    
            except Exception as e:
                print(f"  ⚠️ Timeout/Error esperando contenido: {e}")
            
            # Obtener el HTML renderizado completo
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Buscar productos con todas las palabras importantes
            productos_vistos = set()
            
            # Buscar textos que contengan alguna palabra clave
            patron_busqueda = '|'.join([re.escape(p) for p in palabras_importantes])
            textos_productos = soup.find_all(string=re.compile(patron_busqueda, re.IGNORECASE))
            
            print(f"  📝 Encontrados {len(textos_productos)} textos con palabras clave")
            
            for texto in textos_productos:
                try:
                    contenedor = texto.parent
                    if not contenedor:
                        continue
                    
                    # Verificar que contenga todas las palabras importantes
                    texto_completo = contenedor.get_text().lower()
                    if not all(palabra in texto_completo for palabra in palabras_importantes):
                        continue
                    
                    contenedor_texto = contenedor.get_text()
                    precio_match = re.search(r'\$\s*[\d.,]+', contenedor_texto)
                    
                    if precio_match:
                        precio_texto = precio_match.group()
                        try:
                            precio = self.limpiar_precio(precio_texto)
                        except:
                            continue
                            
                        nombre = self.extraer_nombre_producto(contenedor_texto, precio_texto)
                        
                        # Buscar imagen en el contenedor
                        imagen_url = None
                        img_tag = contenedor.find('img')
                        if img_tag:
                            img_src = img_tag.get('src', '')
                            if img_src and not img_src.startswith('data:'):
                                if img_src.startswith('/'):
                                    imagen_url = f"{self.base_url}{img_src}"
                                elif not img_src.startswith('http'):
                                    imagen_url = f"{self.base_url}/{img_src}"
                                else:
                                    imagen_url = img_src
                        
                        if nombre and precio:
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
                    continue
            
            print(f"  ✅ {len(productos)} productos encontrados que cumplen criterios")
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            import traceback
            traceback.print_exc()
        
        return productos
    
    def limpiar_precio(self, precio_texto: str) -> float:
        """Convertir "$1.236,00" a 1236.00"""
        precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
        return float(precio_limpio)
    
    def extraer_nombre_producto(self, texto: str, precio_texto: str) -> str:
        """Extraer nombre antes del precio"""
        partes = texto.split(precio_texto)
        if len(partes) > 0:
            nombre = partes[0].strip()
            nombre = re.sub(r'OFERTA|DTO\s*\d+%|AGREGAR|VER\s*MAS', '', nombre, flags=re.IGNORECASE).strip()
            # Limpiar espacios múltiples
            nombre = re.sub(r'\s+', ' ', nombre)
            return nombre
        return ""
    
    def __del__(self):
        """Cerrar driver al destruir el objeto"""
        self._close_driver()
