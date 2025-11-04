#!/usr/bin/env python3
"""
Guardar HTML de La Gallega para análisis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("🔍 Abriendo La Gallega y guardando HTML...\n")

options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = uc.Chrome(options=options)

try:
    driver.get("https://lagallega.com.ar")
    print("✅ Página cargada")
    
    # Esperar el div
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "fArticulos"))
    )
    print("✅ Div fArticulos encontrado")
    
    # Esperar más tiempo para AJAX
    print("⏳ Esperando carga completa...")
    time.sleep(5)
    
    # Guardar HTML
    html = driver.page_source
    with open('lagallega_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML guardado en lagallega_debug.html ({len(html)} caracteres)")
    
    # Ver contenido del div fArticulos
    articulos_div = driver.find_element(By.ID, "fArticulos")
    print(f"\n📦 Contenido del div fArticulos:")
    print(f"   Longitud: {len(articulos_div.text)} caracteres")
    print(f"   Primeros 500 caracteres:\n{articulos_div.text[:500]}")
    
finally:
    driver.quit()
    print("\n✅ Navegador cerrado")
