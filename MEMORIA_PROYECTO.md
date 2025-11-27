# MEMORIA DEL PROYECTO - PreciosCerca

## 🎯 VISIÓN Y OBJETIVO DEL PROYECTO

### ¿Qué es PreciosCerca?
**App Android para comparar precios en supermercados argentinos y armar listas de compra inteligentes.**

### Propuesta de valor para el usuario
1. **Saber cuánto va a gastar ANTES de ir al supermercado**
2. **Armar lista digital** con productos reales (nombre, precio, imagen)
3. **Buscar productos específicos** rápidamente
4. **Ver el total en tiempo real** mientras arma la lista
5. **Marcar productos comprados** en el super (se ponen en gris)
6. **Compartir lista por WhatsApp**

### ⚠️ **REGLA FUNDAMENTAL DEL PROYECTO**

**LA APP DEBE SER ESCALABLE A NIVEL NACIONAL**

Actualmente:
- ✅ **Funcionando**: Rosario (4 supermercados: Carrefour, Día %, La Gallega, La Reina)
- 🎯 **Objetivo**: Toda Argentina

**CADA FEATURE/CÓDIGO DEBE PERMITIR:**
1. ✅ Agregar nuevos supermercados fácilmente
2. ✅ Soportar múltiples ciudades/provincias
3. ✅ Escalar sin romper lo existente
4. ❌ **NUNCA** hardcodear solo para Rosario
5. ❌ **NUNCA** asumir que solo hay 4 supermercados

**Supermercados a agregar (prioridad):**
- Coto (Buenos Aires)
- Disco/Jumbo (Cadenas nacionales)
- Walmart/Changomas (Nacional)
- Supermercados regionales por provincia

### Lo que NO es (para no perder foco)
- ❌ **No compara precios ENTRE supermercados** (el usuario elige UNO por lista)
- ❌ **No es e-commerce** (no se compra desde la app)
- ❌ **No requiere cuenta/login** (todo local, privacidad primero)
- ❌ **No usa GPS obligatorio** (el usuario elige supermercado manualmente)

---

## 📋 ÍNDICE
1. [Problemas Resueltos y Soluciones](#problemas-resueltos)
2. [Decisiones de Arquitectura](#decisiones-arquitectura)
3. [Configuración Crítica](#configuracion-critica)
4. [Errores Comunes y Cómo Evitarlos](#errores-comunes)
5. [Scripts de Mantenimiento](#scripts-mantenimiento)

---

## 🔧 PROBLEMAS RESUELTOS Y SOLUCIONES

### 1. PROBLEMA: Búsqueda de "pan" solo encuentra 1 producto (RESUELTO 3 VECES)

**Historia del problema:**

#### Primera iteración (Día 1):
- **Síntoma:** Buscar "pan" encontraba "emPANada", "camPANa"
- **Causa:** Búsqueda simple con `if query in nombre`
- **Solución:** Cambiar a `if ' ' + query + ' ' in ' ' + nombre + ' '`
- **Resultado:** Funcionó pero muy restrictivo

#### Segunda iteración (Día 2):
- **Síntoma:** Buscar "pan" NO encontraba "pan lactal" ni "bizcochos de pan"
- **Causa:** Buscaba `" pan "` (con espacios antes Y después), rechazando "pan lactal"
- **Solución:** Cambiar a buscar `" pan"` (solo espacio antes)
- **Resultado:** Funcionó pero solo en scraper, no en caché

#### Tercera iteración (Día 3 - HOY):
- **Síntoma:** Scraper corregido pero caché seguía con lógica antigua
- **Causa:** Caché y endpoint `/sugerencias` tenían lógica desactualizada
- **Solución DEFINITIVA:**

```python
# PATRÓN CORRECTO - Aplicado en 3 lugares:
# 1. scraper_lagallega.py
# 2. cache_manager.py
# 3. simple_server.py (endpoint /sugerencias)

# Para query de una palabra: "pan"
nombre_lower = ' ' + nombre.lower() + ' '
tiene_todas = True
for palabra in palabras_query:
    if ' ' + palabra not in nombre_lower:  # Solo espacio ANTES
        tiene_todas = False
        break

# Esto acepta:
# ✅ "pan lactal" → " pan lactal "
# ✅ "bizcochos de pan" → " bizcochos de pan "
# ✅ "pan x kg" → " pan x kg "
# ❌ "emPANada" → " empanada " (NO tiene " pan")
# ❌ "campana" → " campana " (NO tiene " pan")
```

**REGLA DE ORO:**
- Patrón: `*palabra1*palabra2*palabra3*`
- Ejemplo 1: `"pan"` → busca `" pan"` (espacio antes, nada después)
- Ejemplo 2: `"dulce de leche"` → busca `" dulce"` Y `" leche"` (todas presentes)

---

### 2. PROBLEMA: Solo 1 producto aparece incluso con scraping correcto

**Causa raíz:** El scraper buscaba en web pero el caché tenía un threshold de 20 productos. Como había 1 en caché (< 20), intentaba buscar en web pero la lógica de filtrado fallaba.

**Solución:** Sistema de precarga completa del catálogo

```python
# En scraper_lagallega.py
total_en_cache = len(cache_manager.cache['productos'].get('lagallega', {}))

if total_en_cache > 500:
    # Caché completo precargado → búsqueda instantánea
    return self._formatear_productos_cache(productos_cache)
else:
    # Caché incompleto → buscar en web (lento)
```

**Script creado:** `backend/precargar_lagallega.py`
- Descarga las 136 categorías completas
- Guarda ~2000-5000 productos
- Solo URLs (no imágenes)
- Ejecutar UNA VEZ, después búsquedas instantáneas

---

### 3. PROBLEMA: Logo de Carrefour incorrecto (RESUELTO 2 VECES)

**Primera vez:** Logo mostraba "DAR" en vez de Carrefour
**Segunda vez:** Después de corrección, seguía mostrando DAR

**Causa:** El archivo `drawable/logo_carrefour.png` no se actualizaba correctamente

**Solución definitiva:**
```powershell
# Siempre copiar Y recompilar con clean
Copy-Item "Logos\carrefour.jpg" "android\app\src\main\res\drawable\logo_carrefour.png" -Force
cd android
.\gradlew.bat clean assembleDebug
```

**NOTA:** No confiar en `assembleDebug` solo, siempre usar `clean` primero si hay cambios en resources.

---

### 4. PROBLEMA: Búsqueda lenta en La Gallega

**Evolución del problema:**

1. **Inicial:** Recorría 136 categorías → 15-20 segundos
2. **Primera optimización:** Solo 20 categorías principales → 5-8 segundos
3. **Segunda optimización:** Caché parcial (> 20 productos) → Inconsistente
4. **Solución DEFINITIVA:** Precarga completa del catálogo → < 100ms

**Archivos involucrados:**
- `backend/precargar_lagallega.py` - Script de precarga
- `backend/PRECARGA_LAGALLEGA.md` - Instrucciones
- `backend/cache_manager.py` - Gestión de caché
- `backend/productos_cache.json` - Base de datos en JSON

---

### 5. PROBLEMA: Error 206 en autoprecarga de Carrefour y Día (RESUELTO - 26 Nov 2025)

**Síntoma:** Al intentar autoprecarga con búsquedas por alfabeto (a-z) o palabras comunes, las APIs VTEX devuelven Error 206 (Partial Content) y 0 productos guardados.

**Causa raíz:** Las APIs VTEX de Carrefour y Día están diseñadas para búsquedas específicas con contexto real, no para scraping masivo. Intentar descargar el catálogo completo mediante queries genéricas (letras sueltas, paginación sin query) activa protecciones anti-scraping.

**Intentos fallidos:**
1. Paginación con `O=OrderByTopSaleDESC` → Error 206
2. Búsqueda por letras individuales (a-z) → Error 206 
3. Búsqueda por palabras comunes directamente a la API → Error 206

**Solución DEFINITIVA:**
```python
# En _auto_precargar() de scraper_carrefour.py y scraper_dia.py

def _auto_precargar(self):
    """Usa el método buscar_productos() que YA FUNCIONA"""
    
    queries = [
        'leche', 'pan', 'yogur', 'queso', 'manteca', 'dulce de leche',
        'aceite', 'arroz', 'fideos', 'harina', 'azucar', 'sal',
        'cafe', 'te', 'mate', 'yerba', 'galletas', 'cerveza',
        'agua', 'gaseosa', 'jugo', 'vino', 'carne', 'pollo'
    ]  # 24 búsquedas reales que la gente usa
    
    for palabra in queries:
        # Usar buscar_productos() que maneja la API correctamente
        productos = self.buscar_productos(palabra)
        # Ya cachea automáticamente, sin Error 206
```

**Por qué funciona:**
- `buscar_productos()` usa la misma lógica que las búsquedas normales del usuario
- Las APIs VTEX aceptan estas búsquedas como legítimas
- El caché se llena progresivamente con productos reales
- No necesita descargar TODO el catálogo, solo lo más común

**Ventajas:**
- ✅ Sin Error 206
- ✅ Más rápido: 3-5 minutos (vs 10-15 minutos intentando)
- ✅ Productos relevantes (los que la gente realmente busca)
- ✅ Caché se sigue llenando con cada búsqueda del usuario

**Archivos modificados:**
- `backend/productos/scrapers/scraper_carrefour.py` - Método `_auto_precargar()`
- `backend/productos/scrapers/scraper_dia.py` - Método `_auto_precargar()`

**REGLA CRÍTICA:** No intentar descargar catálogos completos de APIs VTEX. Usar búsquedas reales y dejar que el caché crezca orgánicamente.

---

## 🏗️ DECISIONES DE ARQUITECTURA

### REGLA #3: Solo URLs, NO descargar imágenes

**Decisión:** El backend NO descarga ni procesa imágenes, solo guarda URLs.

**Razón:**
- Descargar imágenes: 500MB+ de espacio
- Solo URLs: < 5MB de JSON
- Android + Glide cacheará eficientemente

**Implementación:**
```python
# En cache_manager.py y todos los scrapers
cache_manager.agregar_producto(
    supermercado='lagallega',
    nombre=nombre,
    categoria=categoria,
    precio=precio,
    url=producto_url,
    imagen_url=imagen_url  # SOLO URL, no descarga
)
```

**NUNCA usar:**
- ❌ PIL/Pillow para procesar imágenes
- ❌ requests para descargar imágenes
- ❌ Optimización/resize de imágenes
- ❌ Conversión a WebP

---

### Sistema de Caché en 3 Niveles

**Nivel 1: Caché completo precargado (La Gallega)**
- Archivo: `productos_cache.json`
- Método: `precargar_lagallega.py`
- Búsqueda: < 100ms
- Actualización: Manual cada 7-15 días

**Nivel 2: Caché inteligente (Carrefour, Día)**
- API VTEX directa (rápida)
- Caché complementa, no reemplaza
- Threshold: 20 productos

**Nivel 3: Sin caché (La Reina)**
- Scraping HTML tradicional
- 9 categorías
- Búsqueda: 3-5 segundos

### ⚠️ Arquitectura Escalable para Expansión Nacional

**IMPORTANTE:** El código DEBE permitir agregar supermercados sin refactorizar todo.

**Patrón actual (CORRECTO):**
```python
# simple_server.py - Diccionario de scrapers
scrapers = {
    'carrefour': ScraperCarrefour(),
    'dia': ScraperDia(),
    'lareina': ScraperLaReina(),
    'lagallega': ScraperLaGallega()
}
# ✅ Para agregar Coto: solo agregar 'coto': ScraperCoto()
```

**Lo que NO hacer:**
```python
# ❌ MAL - Hardcodear supermercados
if supermercado == "carrefour":
    # código carrefour
elif supermercado == "dia":
    # código día
# Esto NO escala a 50+ supermercados
```

**Checklist para agregar nuevo supermercado:**
1. Crear `scraper_[nombre].py` heredando de `BaseScraper`
2. Implementar `buscar_productos(query)` y `_auto_precargar()`
3. Agregar al diccionario `scrapers` en `simple_server.py`
4. Agregar logo en `android/app/src/main/res/drawable/`
5. Agregar a la lista de botones en `SeleccionSuperActivity.kt`
6. ✅ Listo - sin tocar lógica existente

---

### Búsqueda con Word Boundaries

**Patrón implementado en 3 lugares:**

1. `productos/scrapers/scraper_lagallega.py` líneas ~213-225
2. `cache_manager.py` líneas ~117-130
3. `simple_server.py` endpoint `/sugerencias` líneas ~518-528

**Código exacto que funciona:**
```python
nombre_lower = ' ' + nombre.lower() + ' '
tiene_todas = True
for palabra in palabras_query:
    if ' ' + palabra not in nombre_lower:
        tiene_todas = False
        break
```

**NO cambiar esta lógica sin probar exhaustivamente.**

---

## ⚙️ CONFIGURACIÓN CRÍTICA

### Variables de Entorno

```powershell
# SIEMPRE usar el JBR de Android Studio
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"

# Python del entorno virtual
& C:\PreciosCercaProject\.venv\Scripts\python.exe
```

### Rutas Importantes

```
Backend:
- Server: C:\PreciosCercaProject\backend\simple_server.py
- Caché: C:\PreciosCercaProject\backend\productos_cache.json
- Scrapers: C:\PreciosCercaProject\backend\productos\scrapers\

Android:
- APK: android\app\build\outputs\apk\debug\app-debug.apk
- Logos: android\app\src\main\res\drawable\logo_*.png
- Layouts: android\app\src\main\res\layout\

Logos originales:
- C:\PreciosCercaProject\Logos\*.jpg
```

### Compilación Android

```powershell
cd C:\PreciosCercaProject\android
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"

# Para cambios en código Kotlin
.\gradlew.bat assembleDebug

# Para cambios en resources (logos, layouts)
.\gradlew.bat clean assembleDebug
```

### Servidor Flask

```powershell
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe simple_server.py

# Servidor corre en:
# - http://127.0.0.1:8000
# - http://192.168.100.3:8000 (red local)
```

---

## 🚫 ERRORES COMUNES Y CÓMO EVITARLOS

### Error 1: "Solo encuentra 1 producto"

**Diagnóstico:**
```powershell
# Ver cuántos productos hay en caché
curl "http://192.168.100.3:8000/cache/stats"

# Si total_lagallega < 500 → Ejecutar precarga
```

**Solución:**
```powershell
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe precargar_lagallega.py
```

---

### Error 2: Logo de Carrefour incorrecto

**Causa:** Gradle cachea resources antiguos

**Solución SIEMPRE:**
```powershell
# 1. Copiar logo correcto
Copy-Item "Logos\carrefour.jpg" "android\app\src\main\res\drawable\logo_carrefour.png" -Force

# 2. Clean + Build (NO solo build)
cd android
.\gradlew.bat clean assembleDebug
```

---

### Error 3: Búsqueda encuentra palabras incorrectas (ej: "pan" → "empanada")

**Causa:** Lógica de word boundary incorrecta

**Verificar en 3 archivos:**

1. `scraper_lagallega.py` línea ~217:
```python
if ' ' + palabra not in nombre_lower:  # ✅ Correcto
```

2. `cache_manager.py` línea ~125:
```python
if ' ' + palabra not in nombre_lower:  # ✅ Correcto
```

3. `simple_server.py` línea ~522:
```python
if ' ' + query in nombre_lower:  # ✅ Correcto para autocomplete
```

**NUNCA usar:**
```python
if ' ' + palabra + ' ' in nombre_lower:  # ❌ Demasiado restrictivo
if palabra in nombre_lower:  # ❌ No tiene word boundary
```

---

### Error 4: Servidor Flask no se detiene

```powershell
# Detener TODOS los procesos Python
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Verificar que no hay procesos
Get-Process python -ErrorAction SilentlyContinue
```

---

### Error 5: APK no refleja cambios

**Causa:** Build incremental corrupto

**Solución:**
```powershell
cd android
.\gradlew.bat clean
.\gradlew.bat assembleDebug

# Verificar fecha de modificación del APK
Get-Item "app\build\outputs\apk\debug\app-debug.apk" | Select-Object LastWriteTime
```

---

## 🔄 SCRIPTS DE MANTENIMIENTO

### Precarga semanal del catálogo

```powershell
# Ejecutar cada 7-15 días para actualizar precios
cd C:\PreciosCercaProject\backend
Remove-Item "productos_cache.json" -Force
& C:\PreciosCercaProject\.venv\Scripts\python.exe precargar_lagallega.py
```

### Limpiar y reconstruir todo

```powershell
# Backend: Limpiar caché
cd C:\PreciosCercaProject\backend
Remove-Item "productos_cache.json" -Force

# Android: Limpiar build
cd C:\PreciosCercaProject\android
.\gradlew.bat clean

# Reconstruir APK
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
.\gradlew.bat assembleDebug
```

### Verificar estado del sistema

```powershell
# 1. Verificar servidor
curl "http://192.168.100.3:8000/health"

# 2. Verificar caché
curl "http://192.168.100.3:8000/cache/stats"

# 3. Probar búsqueda
curl "http://192.168.100.3:8000/products?query=pan&supermercado=lagallega"

# 4. Verificar APK
Test-Path "android\app\build\outputs\apk\debug\app-debug.apk"
```

---

## 📊 ESTADÍSTICAS DEL PROYECTO

### Productos por Supermercado

| Supermercado | Categorías | Productos Estimados | Método                    | Velocidad |
|--------------|------------|---------------------|---------------------------|-----------|
| La Gallega   | 136        | 2000-5000           | Precarga completa         | < 100ms   |
| Carrefour    | 24 palabras| 500-1500            | Autoprecarga incremental  | 1-2s      |
| Día %        | 24 palabras| 500-1500            | Autoprecarga incremental  | 1-2s      |
| La Reina     | 212        | 1000-2000           | Autoprecarga HTML         | 3-5s      |

### Archivos Importantes y Su Tamaño

| Archivo                  | Tamaño Típico | Descripción                    |
|--------------------------|---------------|--------------------------------|
| productos_cache.json     | 2-5 MB        | Caché completo de productos    |
| app-debug.apk            | 5-8 MB        | APK de la aplicación Android   |
| simple_server.py         | ~20 KB        | Servidor Flask principal       |
| scraper_lagallega.py     | ~15 KB        | Scraper de La Gallega          |

---

## 🎯 PRÓXIMOS PASOS Y MEJORAS PENDIENTES

### 🚀 Alta Prioridad - EXPANSIÓN NACIONAL
- [ ] **Agregar Coto** (Buenos Aires - cadena importante)
- [ ] **Agregar Disco/Jumbo** (Nacional - grupo Día)
- [ ] **Agregar Walmart/Changomas** (Nacional)
- [ ] **Sistema de selección de provincia/ciudad** en la app
- [ ] **Scrapers para supermercados regionales** (por demanda de usuarios)

### Alta Prioridad - Infraestructura
- [x] Implementar precarga para Carrefour y Día (26 Nov 2025 - Autoprecarga incremental)
- [ ] Sistema de actualización automática del caché (cron job)
- [ ] Logs estructurados con timestamps
- [ ] **Base de datos real** (SQLite/PostgreSQL) en vez de JSON para escalar

### Media Prioridad
- [ ] Dashboard web para ver estado del caché
- [ ] Estadísticas de búsquedas más populares
- [ ] Sistema de notificaciones cuando hay errores
- [ ] **Detección automática de ubicación** (GPS opcional)

### Baja Prioridad
- [ ] Optimizar tamaño del APK
- [ ] Implementar tests automatizados
- [ ] Dockerizar el backend
- [ ] Historial de precios (gráficos de evolución)

---

## 📝 NOTAS FINALES

### Comandos más usados

```powershell
# Iniciar desarrollo
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe simple_server.py

# Compilar Android
cd C:\PreciosCercaProject\android
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
.\gradlew.bat assembleDebug

# Precarga semanal
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe precargar_lagallega.py
```

### Contactos y Referencias

- Backend Framework: Flask 3.0
- Android: Kotlin + Material3
- Python: 3.13.7 (venv)
- Gradle: 8.12
- Java: Android Studio JBR

---

**Última actualización:** 26 de Noviembre, 2025
**Versión de este documento:** 1.1 (Agregada solución Error 206 Carrefour/Día)
