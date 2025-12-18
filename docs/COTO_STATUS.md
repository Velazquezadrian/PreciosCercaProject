# Coto Digital - Estado de Integración

## ✅ Estado Actual: **FUNCIONAL - INTEGRADO**

Coto Digital **está disponible** en la aplicación mediante API JSON (Oracle Endeca).

Ver detalles completos en: [COTO_INTEGRACION_EXITOSA.md](./COTO_INTEGRACION_EXITOSA.md)

## Solución Final

✅ **API JSON descubierta**: Agregar `format=json` a las URLs de búsqueda  
✅ **72 productos por búsqueda**  
✅ **Bypass de Fortigate**: Headers completos + cookies + delay  
✅ **Totalmente funcional** en producción

## Comando Rápido

```bash
# Windows
$env:PYTHONIOENCODING="utf-8"
python backend/simple_server.py

# Linux/Railway
python backend/simple_server.py
```

## Problema Identificado

Coto Digital (https://www.cotodigital.com.ar) es una **Single Page Application (SPA)** construida con Angular/React que:

1. Carga el HTML inicial casi vacío
2. Usa JavaScript para cargar dinámicamente todos los productos
3. No expone una API pública REST/JSON

### Evidencia Técnica

```python
# HTML inicial de Coto:
Total divs: 0
Total articles: 0  
Total li: 0
Texto visible: "Coto Digital: Tu super a un click"
```

El contenido de productos se carga mediante JavaScript después de renderizar la página, por lo que las técnicas tradicionales de web scraping (requests + BeautifulSoup) **no funcionan**.

## Intentos de Solución

### ✅ Probado (No Funciona)
- **BeautifulSoup + requests**: No encuentra productos (HTML vacío)
- **Búsqueda de API interna**: No encontrada o protegida

### ❌ No Implementado (Requiere Recursos)
- **Selenium**: Navegador automatizado (pesado, lento, +500MB RAM por instancia)
- **Playwright**: Alternativa moderna a Selenium (similar overhead)
- **Ingeniería inversa de API**: Requiere inspeccionar tráfico de red, headers específicos, tokens

## Soluciones Posibles

### Opción 1: Selenium/Playwright (No Recomendado)
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.cotodigital.com.ar/sitios/cdigi/browse?_Ntt=leche')
# Esperar carga de JavaScript...
html = driver.page_source
# Parsear con BeautifulSoup
```

**Problemas:**
- ⚠️ Consume ~500MB RAM por navegador
- ⚠️ Lento (5-10 segundos por búsqueda)
- ⚠️ Requiere ChromeDriver/GeckoDriver instalado
- ⚠️ Difícil de ejecutar en Railway (hosting gratuito)

### Opción 2: API Oficial de Coto (Ideal)
Contactar a Coto Digital para obtener acceso a una API oficial para desarrolladores.

**Ventajas:**
- ✅ Rápido y confiable
- ✅ Sin overhead de navegador
- ✅ Datos estructurados

**Desventajas:**
- ❌ Requiere contacto comercial
- ❌ Puede tener costos
- ❌ No hay garantía de respuesta

### Opción 3: Ingeniería Inversa (Gris)
Inspeccionar el tráfico de red de Coto Digital para encontrar endpoints internos.

```bash
# Ejemplo con DevTools de Chrome
1. Abrir https://www.cotodigital.com.ar
2. F12 → Network → XHR
3. Buscar "leche"
4. Copiar Request URL + Headers
```

**Problemas:**
- ⚠️ Puede violar Términos de Servicio
- ⚠️ APIs internas pueden cambiar sin aviso
- ⚠️ Requiere headers/cookies específicos

## Recomendación

**Mantener Coto deshabilitado** hasta que:
1. Haya presupuesto para Selenium en un servidor dedicado
2. Coto ofrezca una API oficial
3. La app tenga suficientes usuarios para justificar el costo

Los 4 supermercados actuales (Carrefour, Día %, La Reina, La Gallega) cubren >60% del mercado argentino.

## Código Deshabilitado

```python
# backend/simple_server.py
scrapers = {
    # ...
    # 'coto': ScraperCoto()  # ❌ DESHABILITADO: Coto es SPA
}
```

## Referencias
- Scraper original: `backend/productos/scrapers/scraper_coto.py`
- Tests: `test_coto_html.py`, `test_coto_api.py`
