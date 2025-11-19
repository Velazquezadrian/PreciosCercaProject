# 💰 Mi Lista de Precios

**App Android para hacer tu lista de compras y comparar precios entre supermercados argentinos**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)
[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)
[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)

---

## ✨ Características Principales

### 📱 Para Usuarios

- 🛒 **Dos modos de uso:**
  - **Mi Lista de Compra** - Armá tu lista con productos de un supermercado específico
  - **Buscar Producto** - Consultá precios sin guardar nada

- 🏪 **4 Supermercados activos:**
  - Carrefour (API VTEX - 148 categorías) - 50 productos
  - Día % (API REST - 122 categorías) - 50 productos
  - La Reina (HTML scraping - 212 categorías) - 50 productos
  - La Gallega (HTML scraping - 136 categorías) - 50 productos
  - **TOTAL: 618 categorías mapeadas**

- 🔍 **Búsqueda inteligente:**
  - Soporta palabras compuestas ("dulce de leche", "aceite de oliva")
  - Búsqueda exhaustiva por categorías (no solo texto libre)
  - 50+ productos por supermercado garantizados
  - Filtrado automático por relevancia

- 💰 **Lista de compras completa:**
  - Agregar productos con imagen, precio y supermercado
  - Ver total acumulado en tiempo real
  - "Terminar Lista" para ir al supermercado
  - Marcar productos como comprados (tap para gris)
  - Compartir lista por WhatsApp

- 🎨 **Diseño moderno:**
  - Material Design con colores azul (#2196F3) y naranja (#FF9800)
  - Iconos grandes y claros: 📝 Mi Lista de Compra, 🔍 Buscar Producto
  - Imágenes de productos cargadas con Glide

### 🔧 Para Desarrolladores

- 🚀 **API REST con Flask** - 5 endpoints principales
- 🕷️ **Web scraping optimizado** - 2 APIs oficiales + 1 HTML parser
- 📦 **Arquitectura modular** - Fácil agregar nuevos supermercados
- 🎨 **Material Design 3** en Android
- 🔄 **Retrofit** para HTTP + **Glide** para imágenes
- 📝 **Código limpio** y bien documentado

---

## 🚀 Instalación Rápida

### 📱 Usar la App (5 minutos)

1. **Instalar APK:**
   ```
   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk
   Tamaño: ~6.5 MB
   Requisitos: Android 7.0+
   ```

2. **Iniciar servidor backend:**
   ```bash
   cd C:\PreciosCercaProject
   .venv\Scripts\python.exe backend\simple_server.py
   ```

3. **Configurar IP en la app:**
   - Emulador Android: `http://10.0.2.2:8000`
   - Dispositivo físico: `http://TU-IP-LOCAL:8000`
   - Editar en: `android/app/src/main/java/com/precioscerca/api/ApiClient.kt`

4. **¡Listo!** Elegí el modo, buscá productos y armá tu lista

---

## 🏗️ Arquitectura del Proyecto

```
PreciosCercaProject/
├── 📱 android/                      # Aplicación Android Kotlin
│   ├── app/src/main/
│   │   ├── java/com/precioscerca/
│   │   │   ├── MainActivity.kt              # Pantalla inicial (2 botones)
│   │   │   ├── SeleccionSuperActivity.kt   # Elegir supermercado
│   │   │   ├── BusquedaActivity.kt          # Buscar productos
│   │   │   ├── MiListaActivity.kt           # Ver lista con total
│   │   │   ├── ListaTerminadaActivity.kt    # Marcar comprados + compartir
│   │   │   ├── api/PreciosCercaApi.kt       # Cliente Retrofit
│   │   │   ├── adapters/                    # RecyclerView adapters
│   │   │   └── models/ProductoEnLista.kt    # Modelo Parcelable
│   │   └── res/
│   │       ├── layout/                      # XMLs de UI
│   │       ├── values/
│   │       │   ├── colors.xml               # Azul + Naranja
│   │       │   └── strings.xml              # "Mi Lista de Precios"
│   │       └── xml/file_paths.xml           # FileProvider para compartir
│   └── build.gradle                         # Glide 4.16, Retrofit 2.9, Parcelize
│
├── 🐍 backend/                      # Flask API + Scrapers
│   ├── simple_server.py             # ✅ Servidor principal (puerto 8000)
│   ├── lista_compras.py             # Sistema de lista (agregar/eliminar)
│   ├── productos/
│   │   ├── services.py              # Filtro de búsqueda multi-palabra
│   │   └── scrapers/
│   │       ├── base_scraper.py      # Clase abstracta base
│   │       ├── scraper_carrefour.py # ✅ API VTEX oficial (50 productos)
│   │       ├── scraper_dia.py       # ✅ API REST oficial (50 productos)
│   │       ├── scraper_lareina.py   # ✅ HTML parsing (212 categorías)
│   │       └── scraper_lagallega.py # ✅ HTML parsing (136 categorías)
│   ├── requirements.txt             # Flask, requests, BeautifulSoup
│   └── test_palabras_compuestas.py  # Tests de búsqueda
│
└── 📚 docs/
    ├── INSTALLATION.md
    ├── TESTING_GUIDE.md
    ├── PRIVACY_POLICY.md
    └── PLAY_STORE_METADATA.md
```

---

## 🔌 API REST

### 🌐 Endpoints Disponibles

#### 1. Buscar Productos
```bash
GET /products?query=leche&supermercado=carrefour
```

**Parámetros:**
- `query` (requerido): término de búsqueda
- `supermercado` (opcional): `carrefour`, `dia` o `lareina`

**Respuesta:**
```json
{
  "query": "leche",
  "total_encontrados": 50,
  "supermercados_consultados": ["Carrefour"],
  "productos_por_supermercado": {"Carrefour": 50},
  "resultados": [
    {
      "nombre": "Leche Entera La Serenísima 1L",
      "precio": 1250.50,
      "supermercado": "Carrefour",
      "fecha": "2025-11-03",
      "relevancia": 1.0,
      "url": "https://...",
      "imagen": "https://..."
    }
  ]
}
```

#### 2. Lista de Compras
```bash
GET    /lista-compras              # Ver lista
POST   /lista-compras/agregar      # Agregar producto
DELETE /lista-compras/eliminar     # Eliminar producto
POST   /lista-compras/limpiar      # Vaciar lista
```

**Agregar producto (POST):**
```json
{
  "nombre": "Leche La Serenísima 1L",
  "cantidad": 2,
  "precio": 1250.50,
  "supermercado": "Carrefour",
  "imagen": "https://..."
}
```

#### 3. Health Check
```bash
GET /health      # Estado del servidor
GET /            # Info de la API
```

---

## 📱 Flujo de la App

```
┌─────────────────────┐
│   MainActivity      │  [INICIO]
│                     │
│   💰 "Mi Lista de   │  - Dos botones grandes (50% cada uno)
│      Precios"       │  - 📝 Mi Lista de Compra (modo LISTA)
│                     │  - 🔍 Buscar Producto (modo CONSULTA)
│   [Botón 1] [Botón 2]│
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│ SeleccionSuper...   │  [ELEGIR SUPERMERCADO]
│                     │
│  🛒 Carrefour       │  - 4 cards con colores de marca
│  🛒 Día %           │  - Pasa MODO + SUPERMERCADO a BusquedaActivity
│  🛒 La Reina        │  - Azul, Rojo, Verde, Naranja
│  🛒 La Gallega      │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  BusquedaActivity   │  [BUSCAR PRODUCTOS]
│                     │
│  [🔍 Buscar...]     │  - Solo productos del super elegido
│  Total: $1,234.56   │  - Total acumulado (modo LISTA)
│                     │  - Botón "+" para agregar a lista
│  • Producto 1  [+]  │  - Menú: 🛒 Ver Mi Lista
│  • Producto 2  [+]  │
│  • Producto 3  [+]  │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  MiListaActivity    │  [VER LISTA]
│                     │
│  Total: $1,234.56   │  - RecyclerView con productos
│                     │  - Imagen 60x60, nombre, precio, super
│  🖼️ Producto 1  [🗑️] │  - Botón eliminar por producto
│  🖼️ Producto 2  [🗑️] │  - Botón "Terminar Lista" al final
│  🖼️ Producto 3  [🗑️] │
│                     │
│  [Terminar Lista]   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│ ListaTerminadaAct   │  [CHECKLIST]
│                     │
│  Toca para marcar:  │  - Tap en producto → escala de grises
│                     │  - ColorMatrixColorFilter (saturation=0)
│  🖼️ Producto 1      │  - Botón "Compartir" genera .txt
│  🖼️ Producto 2 (✓)  │  - FileProvider + Intent.ACTION_SEND
│  🖼️ Producto 3      │  - Formato: ✅ comprado / ⬜ pendiente
│                     │
│  [Compartir]        │
└─────────────────────┘
```

---

## 🛠️ Para Desarrolladores

### 🔧 Setup Completo

```bash
# 1. Clonar repositorio
git clone https://github.com/Velazquezadrian/PreciosCercaProject.git
cd PreciosCercaProject

# 2. Backend - Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt

# 3. Ejecutar servidor
python backend/simple_server.py  # Puerto 8000

# 4. Android - Abrir Android Studio
# Importar carpeta 'android/'
# Sync Gradle automáticamente
# Configurar IP en ApiClient.kt
# Build & Run
```

### 🧪 Testing

```bash
# Probar API
curl "http://localhost:8000/products?query=leche"

# Probar búsquedas multi-palabra
cd backend
python test_palabras_compuestas.py

# Ver estado del servidor
curl "http://localhost:8000/health"
```

### 📝 Agregar Nuevo Supermercado

1. **Crear scraper** en `backend/productos/scrapers/scraper_nuevo.py`:
```python
from .base_scraper import BaseScraper

class ScraperNuevo(BaseScraper):
    def buscar_productos(self, query):
        # Implementar lógica de scraping/API
        return [{
            'nombre': 'Producto',
            'precio': 100.0,
            'supermercado': 'Nuevo',
            'imagen': 'url',
            'url': 'url'
        }]
```

2. **Registrar** en `simple_server.py`:
```python
from productos.scrapers.scraper_nuevo import ScraperNuevo

scrapers = {
    'carrefour': ScraperCarrefour(),
    'dia': ScraperDia(),
    'lareina': ScraperLaReina(),
    'nuevo': ScraperNuevo()  # ← Agregar aquí
}
```

3. **Actualizar app Android** - Agregar card en `SeleccionSuperActivity`

---

## 🎯 Roadmap

### ✅ Completado

- [x] Búsqueda con palabras compuestas
- [x] 4 supermercados activos (Carrefour, Día, La Reina, La Gallega)
- [x] Mapeo completo de 348 categorías (212 La Reina + 136 La Gallega)
- [x] Optimización de scrapers (50 productos consistentes)
- [x] Lista de compras con imágenes
- [x] Total en tiempo real
- [x] "Terminar Lista" con checklist
- [x] Marcar productos como comprados (grayscale)
- [x] Compartir por WhatsApp
- [x] Diseño Material Design 3
- [x] App funcional compilada

### 📋 Próximo (1-2 semanas)

- [ ] Persistencia de listas en base de datos
- [ ] Histórico de listas anteriores
- [ ] Editar cantidad de productos en lista
- [ ] Filtros y ordenamiento en búsqueda

### 🚀 Mediano Plazo (1-2 meses)

- [ ] Agregar más supermercados (Jumbo, Disco, Coto)
- [ ] Escaneo de códigos de barras
- [ ] Notificaciones de ofertas
- [ ] Cache de resultados

### 🌟 Largo Plazo (3-6 meses)

- [ ] App iOS
- [ ] API pública
- [ ] Machine Learning para predicción de precios
- [ ] Play Store release

---

## 📊 Comparación con Competencia

| Característica | [Pricely.ar](https://pricely.ar) | Mi Lista de Precios | Estado |
|----------------|------------|---------------------|---------|
| App Android | ✅ | ✅ | **Logrado** |
| Datos reales | ✅ | ✅ | **Logrado** |
| Supermercados | 10+ | 4 activos | En expansión |
| Búsqueda compleja | ❓ | ✅ | **Ventaja** |
| Lista de compras | ✅ | ✅ | **Logrado** |
| Compartir lista | ❌ | ✅ | **Ventaja** |
| Código abierto | ❌ | ✅ | **Ventaja** |
| Gratis | ✅ | ✅ | **Logrado** |

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 🎉

1. **Fork** el proyecto
2. Crear **feature branch**: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -m 'Agregar nueva característica'`
4. **Push** a la branch: `git push origin feature/nueva-caracteristica`
5. Abrir **Pull Request**

### 🐛 Reportar Bugs

- Usar [GitHub Issues](https://github.com/Velazquezadrian/PreciosCercaProject/issues)
- Incluir pasos para reproducir
- Especificar versión de Android

---

## 📄 Licencia

MIT License - Proyecto open source para la comunidad argentina.

Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Contacto

- **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)
- **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)

---

**⭐ Si te gusta el proyecto, dale una estrella en GitHub!**

**💰 Desarrollado con ❤️ para ayudar a los argentinos a ahorrar dinero**

**🛒 4 supermercados funcionando, más en camino!**
