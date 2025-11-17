# 🎮 Instrucciones para Probar en BlueStacks

## ✅ Configuración Ya Lista

La app YA está configurada para funcionar con BlueStacks usando la IP `10.0.2.2:8000`

---

## 🚀 Pasos para Probar

### 1️⃣ Iniciar el Backend (Hacelo vos en PowerShell)

```powershell
cd C:\PreciosCercaProject
.venv\Scripts\python.exe backend\simple_server.py
```

Deberías ver:
```
🚀 Inicializando PreciosCerca Server...
✅ Carrefour scraper cargado correctamente
✅ Día % scraper cargado correctamente
✅ La Reina scraper cargado correctamente
...
📍 URL: http://localhost:8000
```

**⚠️ IMPORTANTE: Dejá esta terminal abierta mientras probás la app!**

---

### 2️⃣ Compilar la APK

**Opción A: Desde Android Studio (Recomendado)**

1. Abrí Android Studio
2. Abrí el proyecto: `C:\PreciosCercaProject\android`
3. Esperá que sincronice Gradle (puede tardar 1-2 minutos la primera vez)
4. `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
5. Esperá que compile (aparecerá "Build Successful")
6. Click en el link "locate" que aparece abajo a la derecha
   - O andá manualmente a: `C:\PreciosCercaProject\android\app\build\outputs\apk\debug\`
7. Verás el archivo `app-debug.apk`

**Opción B: Desde Línea de Comandos**

```powershell
cd C:\PreciosCercaProject\android
.\gradlew assembleDebug
```

La APK estará en: `android\app\build\outputs\apk\debug\app-debug.apk`

---

### 3️⃣ Instalar en BlueStacks

1. **Abrí BlueStacks**
2. **Arrastrá el archivo `app-debug.apk`** directamente a la ventana de BlueStacks
3. **Esperá la instalación** (verás un mensaje "App instalada exitosamente")
4. **Buscá el ícono de PreciosCerca** en el menú de apps

---

### 4️⃣ Probar el Flujo Completo

1. **Abrí PreciosCerca** en BlueStacks
2. **Pantalla de inicio:**
   - Deberías ver fondo morado, logo 🛒 y botón "Empezar Lista"
   - Click en **"Empezar Lista"**

3. **Selección de Supermercado:**
   - Verás 3 cards grandes:
     - 🛒 **Carrefour** (azul)
     - 🛒 **Día %** (rojo)
     - 🛒 **La Reina** (verde)
   - Click en cualquiera, por ejemplo **Carrefour**

4. **Búsqueda de Productos:**
   - Verás "Carrefour" en el título
   - Verás campo de búsqueda y "Total: $0.00"
   - Escribí un producto, ej: **"leche"**
   - Click en **"Buscar"**
   - Deberías ver productos SOLO de Carrefour

5. **Verificar en el Backend:**
   - En la terminal de PowerShell donde corre el servidor deberías ver:
   ```
   🔍 Búsqueda: 'leche' en CARREFOUR
     🔍 Buscando en Carrefour...
     ✅ Carrefour: 50 productos
   ✅ 50 productos encontrados
   ```

6. **Ver la Lista:**
   - Click en el ícono **🛒** (arriba a la derecha)
   - Te lleva a la lista de compras

---

## 🎯 Qué Probar

### Test 1: Búsqueda por Supermercado
- Elegí Carrefour → Buscá "leche" → Solo productos de Carrefour ✅
- Volvé atrás → Elegí Día % → Buscá "pan" → Solo productos de Día ✅
- Volvé atrás → Elegí La Reina → Buscá "aceite" → Solo productos La Reina ✅

### Test 2: Flujo Completo
- Empezar Lista → Carrefour → Buscar "arroz" → Agregar productos → Ver lista ✅

### Test 3: Backend
- Verificá en la consola que diga "en CARREFOUR", "en DIA", "en LAREINA" según lo que elegiste

---

## 🐛 Si Algo No Funciona

### ❌ "No se puede conectar al servidor"

**Causas posibles:**
1. El backend no está corriendo
   - Verificá la terminal de PowerShell
   - Deberías ver "Running on http://0.0.0.0:8000"

2. Firewall de Windows
   - Permití Python en el Firewall si te pregunta

3. BlueStacks no puede acceder a localhost
   - Verificá que la app use `10.0.2.2:8000` (ya está configurado)

**Solución rápida:**
```powershell
# Probá el servidor desde el navegador:
Start-Process "http://localhost:8000/health"
```

Deberías ver:
```json
{
  "status": "OK",
  "message": "PreciosCerca Server funcionando",
  "scrapers_disponibles": ["carrefour", "dia", "lareina"]
}
```

### ❌ "La app se cierra sola" (Crash)

1. **Abrí Android Studio**
2. **Conectá BlueStacks:**
   - `Tools` → `Device Manager` → Deberías ver BlueStacks listado
3. **Abrí Logcat:**
   - `View` → `Tool Windows` → `Logcat`
4. **Filtrá por errores:**
   - Buscá líneas en rojo con "Exception" o "Error"
5. **Mandame el error** y te ayudo a solucionarlo

### ❌ "No aparecen productos"

**Verificá:**
1. ¿El backend muestra "Buscando en Carrefour..." cuando buscás?
   - Si SÍ: El scraper está funcionando
   - Si NO: La app no se está conectando

2. ¿Qué dice el backend después de "Buscando..."?
   - Si dice "✅ Carrefour: 50 productos" → El backend funciona bien
   - Si dice "❌ Error..." → Hay problema con el scraper

**Test rápido desde PowerShell:**
```powershell
# Test directo al backend:
Invoke-WebRequest -Uri "http://localhost:8000/products?query=leche&supermercado=carrefour" | Select-Object -Expand Content
```

Deberías ver un JSON con productos.

---

## 📊 Verificaciones Exitosas

Si TODO funciona, deberías ver:

✅ **Backend corriendo** en PowerShell  
✅ **App instalada** en BlueStacks  
✅ **Flujo completo:** Inicio → Selección → Búsqueda → Lista  
✅ **Productos filtrados** por supermercado elegido  
✅ **Total acumulado** visible (aunque sea $0.00 si no agregaste nada)  
✅ **Logs en backend** mostrando las búsquedas  

---

## 🎉 Todo Listo!

La configuración ya está hecha. Solo tenés que:

1. **Arrancar el backend** (vos en PowerShell)
2. **Compilar la APK** (Android Studio o gradlew)
3. **Arrastrar APK a BlueStacks**
4. **¡Probar!**

Si tenés algún problema, avisame con el mensaje de error específico y te ayudo.

---

**Archivo creado:** 2025-11-10  
**Versión de la app:** 2.0 - Lista de Compras
