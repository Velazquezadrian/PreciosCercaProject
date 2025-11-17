# 🛒 PreciosCerca - Tu Lista de Compras Inteligente# 🛒 PreciosCerca - Comparador de Precios de Supermercados



**App Android para hacer tu lista de compras en tu supermercado favorito y controlarla mientras comprás****Aplicación completa para comparar precios entre supermercados argentinos en tiempo real**



[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)

[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)

[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)

[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)



------



## 💡 Concepto de la App## ✨ Estado Actual - ¡FUNCIONANDO!



**PreciosCerca** te ayuda a hacer tu lista de compras de forma inteligente:### ✅ Completado y operativo



1. **📱 Empezás tu lista** - Pantalla de inicio simple con botón "Empezar Lista"- **� App Android** - APK compilada y funcional (6.45MB)

2. **🏪 Elegís tu supermercado** - Carrefour, Día % o La Reina- **�🛒 3 Supermercados activos:**

3. **🔍 Buscás productos** - Solo del supermercado que elegiste  - **Carrefour** - 50+ productos por búsqueda (API VTEX oficial) ✅

4. **➕ Armás tu lista** - Agregás productos y ves el total acumulado  - **Día %** - 50+ productos por búsqueda (API REST oficial) ✅

5. **✅ Finalizás la lista** - Cuando estés listo para ir al super  - **La Reina** - Scraper HTML mejorado ✅

6. **🛒 Usás el checklist** - Tildás productos mientras comprás- **🔍 Búsqueda con palabras compuestas** - "dulce de leche", "aceite de oliva", etc.

- **🖼️ Imágenes de productos** - Carga con Glide desde URLs de supermercados

**Diferencia clave:** A diferencia de comparadores de precios, PreciosCerca te permite enfocarte en UN supermercado y armar tu lista sabiendo exactamente qué vas a gastar.- **🖥️ Servidor Flask** - API REST estable en puerto 8000

- **🛒 Lista de compras** - Agregar/eliminar productos con comparación de precios

---

### 📊 Resultados actuales

## ✨ Estado Actual

- **150+ productos** por búsqueda (50 de cada supermercado)

### ✅ Completado y Funcionando- **3 supermercados** consultados simultáneamente

- **Comparación en tiempo real** con ordenamiento automático por precio

- **📱 Pantalla de inicio** - Botón simple para empezar nueva lista- **Soporte completo** para búsquedas con múltiples palabras

- **🏪 Selección de supermercado** - 3 cards grandes con colores de marca:

  - **Carrefour** (azul) - 50+ productos por búsqueda ✅### 🔄 En desarrollo

  - **Día %** (rojo) - 50+ productos por búsqueda ✅

  - **La Reina** (verde) - 30+ productos por búsqueda ✅- **La Gallega** - Scraper con Selenium (requiere navegación dinámica de JavaScript)

- **🔍 Búsqueda filtrada** - Endpoint `/products?query=X&supermercado=Y`

- **💰 Total en tiempo real** - Suma acumulada visible en pantalla de búsqueda---

- **🖼️ Imágenes de productos** - Carga con Glide desde URLs oficiales

- **📋 Lista de compras** - Agregar/eliminar productos con persistencia## 🚀 Instalación Rápida

- **🖥️ Servidor Flask** - API REST en puerto 8000

### 📱 Usar la App (5 minutos)

### 🔄 Próximamente

1. **Instalar APK:**

- **✅ Modo checklist** - Tildar productos mientras comprás   ```

- **🔒 Lista finalizada** - Bloquear edición al confirmar   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk

- **📊 Resumen de compra** - Total gastado y productos marcados   Tamaño: 6.45MB

   Requisitos: Android 7.0+

---   ```



## 🚀 Instalación Rápida2. **Iniciar servidor backend:**

   ```bash

### Requisitos previos   cd C:\PreciosCercaProject

   .venv\Scripts\python.exe backend\simple_server.py

- Python 3.8+ con `pip`   ```

- Android Studio (para compilar APK) o dispositivo Android 7.0+

- Windows PowerShell o terminal3. **Configurar IP en la app:**

   - Emulador Android: `http://10.0.2.2:8000`

### 1. Configurar Backend   - Dispositivo físico: `http://TU-IP-LOCAL:8000`



```powershell4. **¡Listo!** Busca productos y compara precios entre **Carrefour**, **Día %** y **La Reina**

cd C:\PreciosCercaProject

---

# Crear entorno virtual (si no existe)

python -m venv .venv## 🏗️ Arquitectura del Proyecto



# Activar entorno virtual```

.venv\Scripts\Activate.ps1PreciosCercaProject/

├── 📱 android/                      # Aplicación Android

# Instalar dependencias│   ├── app/src/main/

pip install -r backend\requirements.txt│   │   ├── java/com/precioscerca/

│   │   │   ├── MainActivity.kt       # Pantalla principal con búsqueda aleatoria

# Iniciar servidor│   │   │   ├── ProductListActivity.kt # Resultados de búsqueda

python backend\simple_server.py│   │   │   ├── ListaComprasActivity.kt # Lista de compras

```│   │   │   ├── api/PreciosCercaApi.kt  # Cliente Retrofit

│   │   │   └── adapters/ProductAdapter.kt # RecyclerView con imágenes

El servidor estará en `http://localhost:8000`│   │   └── res/

│   │       ├── layout/

### 2. Instalar App Android│   │       │   ├── activity_main.xml

│   │       │   ├── activity_product_list.xml

**Opción A: APK Pre-compilada** (más rápido)│   │       │   └── item_producto.xml  # Card con imagen 80x80dp

```│   │       └── menu/

Ubicación: android/app/build/outputs/apk/debug/app-debug.apk│   └── build.gradle                 # Dependencias: Glide 4.16.0, Retrofit, etc.

Tamaño: ~6.5MB│

Requisitos: Android 7.0+├── 🐍 backend/                      # Flask API + Web Scrapers

```│   ├── simple_server.py             # ✅ Servidor principal (puerto 8000)

│   ├── lista_compras.py             # Sistema de lista de compras

Transferir al celular e instalar.│   ├── productos/scrapers/

│   │   ├── base_scraper.py          # Clase base para scrapers

**Opción B: Compilar desde Android Studio**│   │   ├── scraper_carrefour.py     # ✅ API VTEX de Carrefour

1. Abrir `android/` en Android Studio│   │   ├── scraper_dia.py           # ✅ API REST de Día

2. Esperar sincronización de Gradle│   │   ├── scraper_lareina.py       # ✅ HTML parsing mejorado

3. Build → Build Bundle(s)/APK(s) → Build APK│   │   ├── scraper_lagallega.py     # 🔄 En desarrollo

4. Instalar en dispositivo│   │   ├── scraper_lagallega_selenium.py # 🔄 Versión con Selenium

│   │   └── sucursales_data.py       # Datos de sucursales (GPS)

### 3. Configurar IP del Servidor│   ├── test_palabras_compuestas.py  # Tests para búsquedas complejas

│   └── requirements.txt             # Flask, requests, BeautifulSoup, Selenium

Editar `PreciosCercaApi.kt`:│

- **Emulador Android:** `http://10.0.2.2:8000`├── 📚 docs/

- **Dispositivo físico:** `http://TU-IP-LOCAL:8000` (ver con `ipconfig`)│   ├── PRIVACY_POLICY.md

│   ├── INSTALLATION.md

---│   ├── TESTING_GUIDE.md

│   └── PLAY_STORE_METADATA.md

## 🏗️ Arquitectura│

└── README.md                        # Este archivo

``````

PreciosCercaProject/

├── 📱 android/                          # App Android en Kotlin---

│   └── app/src/main/

│       ├── java/com/precioscerca/## 📊 API REST Funcionando

│       │   ├── MainActivity.kt           # [INICIO] - Pantalla de bienvenida con logo

│       │   ├── SeleccionSuperActivity.kt # [SELECCIÓN] - Elegir supermercado### 🌐 Endpoints disponibles

│       │   ├── BusquedaActivity.kt       # [BÚSQUEDA] - Buscar en super elegido

│       │   ├── ListaComprasActivity.kt   # [LISTA] - Ver lista y checklist- **`GET /products?query=leche`** - Buscar productos en todos los supermercados ✅

│       │   ├── api/- **`GET /health`** - Estado del servidor ✅

│       │   │   └── PreciosCercaApi.kt    # Cliente Retrofit con filtro supermercado- **`GET /`** - Información de la API ✅

│       │   └── adapters/- **`GET /lista-compras`** - Obtener lista de compras ✅

│       │       └── ProductAdapter.kt      # RecyclerView con imágenes- **`POST /lista-compras/agregar`** - Agregar producto a lista ✅

│       └── res/- **`DELETE /lista-compras/eliminar`** - Eliminar producto de lista ✅

│           ├── layout/- **`GET /lista-compras/comparar`** - Comparar precios de lista completa ✅

│           │   ├── activity_main.xml              # Botón grande centrado

│           │   ├── activity_seleccion_super.xml   # 3 cards de supermercados### 📱 Respuesta de ejemplo

│           │   ├── activity_busqueda.xml          # Búsqueda + total + lista

│           │   └── item_producto.xml              # Card con imagen 80x80dp```json

│           └── menu/{

│               └── menu_busqueda.xml              # Ícono carrito → lista  "query": "dulce de leche",

│  "total_encontrados": 15,

├── 🐍 backend/                          # Flask API + Scrapers  "supermercados_consultados": ["Carrefour", "Día %", "La Reina"],

│   ├── simple_server.py                 # Servidor principal (puerto 8000)  "productos_por_supermercado": {

│   ├── lista_compras.py                 # Sistema de lista global    "Carrefour": 8,

│   ├── productos/scrapers/    "Día %": 5,

│   │   ├── base_scraper.py              # Clase base abstracta    "La Reina": 2

│   │   ├── scraper_carrefour.py         # API VTEX oficial  },

│   │   ├── scraper_dia.py               # API REST oficial  "resultados": [

│   │   ├── scraper_lareina.py           # Scraping HTML    {

│   │   └── sucursales_data.py           # Datos de sucursales      "nombre": "Dulce De Leche Colonial Repostero 1kg",

│   └── requirements.txt                 # Flask, requests, beautifulsoup4      "precio": 2450.50,

│      "supermercado": "Carrefour",

└── 📚 docs/      "fecha": "2025-11-04",

    ├── INSTALLATION.md      "relevancia": 1.0,

    ├── TESTING_GUIDE.md      "url": "https://www.carrefour.com.ar/...",

    ├── PRIVACY_POLICY.md      "imagen": "https://carrefourar.vtexassets.com/..."

    └── PLAY_STORE_METADATA.md    },

```    {

      "nombre": "Dulce de leche La Serenisima 400g",

---      "precio": 1890.00,

      "supermercado": "Día %",

## 🔌 API Endpoints      "fecha": "2025-11-04",

      "relevancia": 1.0,

### `GET /products`      "url": "https://diaonline.supermercadosdia.com.ar/...",

Buscar productos en todos los supermercados o uno específico      "imagen": "https://diaonlinear.vtexassets.com/..."

    }

**Parámetros:**  ]

- `query` (obligatorio): término de búsqueda (ej: "leche", "pan", "dulce de leche")}

- `supermercado` (opcional): filtrar por `carrefour`, `dia` o `lareina````



**Ejemplos:**---

```bash

# Buscar solo en Carrefour## 🎯 Características Principales

curl "http://localhost:8000/products?query=leche&supermercado=carrefour"

### ✨ Para usuarios

# Buscar solo en Día %

curl "http://localhost:8000/products?query=pan&supermercado=dia"- � **Búsqueda inteligente** con palabras compuestas

- 💰 **Comparación de precios** en tiempo real entre 3 supermercados

# Buscar en todos (comportamiento antiguo)- 🖼️ **Imágenes de productos** cargadas directamente de los supermercados

curl "http://localhost:8000/products?query=aceite"- �🛒 **Lista de compras** con comparación automática de precios

```- 📊 **Ordenamiento automático** por precio (más barato primero)

- 🏷️ **Badges especiales** - "MÁS BARATO", "MÁS CERCANO"

**Respuesta:**- 🌐 **Links directos** a productos en sitios web de supermercados

```json

{### 🔧 Para desarrolladores

  "products": [

    {- 🚀 **API REST** bien documentada con Flask

      "nombre": "Leche Entera La Serenísima 1L",- 🕷️ **Web scraping** optimizado (APIs oficiales + HTML parsing)

      "precio": 450.50,- 📦 **Arquitectura modular** - Fácil agregar nuevos supermercados

      "supermercado": "Carrefour",- 🎨 **Material Design 3** en la app Android

      "imagen": "https://carrefourar.vtexassets.com/...",- 🔄 **Retrofit** para llamadas HTTP eficientes

      "unidad": "1 L"- 🖼️ **Glide** para carga optimizada de imágenes

    }- 📝 **Código limpio** y bien documentado

  ],

  "total": 1---

}

```## 🛠️ Para Desarrolladores



### `POST /lista`### 🔧 Setup completo

Agregar producto a la lista de compras

```bash

### `GET /lista`# 1. Clonar repositorio

Obtener lista actualgit clone https://github.com/Velazquezadrian/PreciosCercaProject.git

cd PreciosCercaProject

### `DELETE /lista/<id>`

Eliminar producto de la lista# 2. Backend - Crear entorno virtual

cd backend

---python -m venv ..\\.venv

..\\.venv\\Scripts\\activate

## 🎨 Flujo de Pantallaspip install -r requirements.txt



```# 3. Ejecutar servidor

┌─────────────────────┐python simple_server.py  # Puerto 8000

│   MainActivity      │  [INICIO]

│                     │# 4. Android - Abrir Android Studio

│   🛒 Logo grande    │  - Fondo color primary# Importar proyecto desde carpeta 'android/'

│   "PreciosCerca"    │  - Botón "Empezar Lista"# Sync Gradle automáticamente

│                     │  - Sin búsqueda ni productos# Build & Run

│   [Empezar Lista]   │```

└──────────┬──────────┘

           │### 🧪 Testing

           v

┌─────────────────────┐```bash

│ SeleccionSuper...   │  [SELECCIÓN]# Probar API

│                     │curl "http://localhost:8000/products?query=leche"

│  🛒 Carrefour       │  - 3 cards grandes con colores

│  🛒 Día %           │  - Click → BusquedaActivity# Probar búsquedas con palabras compuestas

│  🛒 La Reina        │  - finish() para evitar backcd backend

│                     │python test_palabras_compuestas.py

└──────────┬──────────┘

           │# Ver estado del servidor

           vcurl "http://localhost:8000/health"

┌─────────────────────┐```

│  BusquedaActivity   │  [BÚSQUEDA]

│                     │### 📱 Configurar app Android

│  [🔍 Buscar...]     │  - Solo productos del super elegido

│  Total: $1,234.56   │  - Total acumulado arriba1. **Abrir Android Studio**

│                     │  - RecyclerView con productos2. **Importar proyecto**: carpeta `android/`

│  • Producto 1       │  - Botón "+" agrega a lista3. **Sync Gradle** (automático)

│  • Producto 2       │  - Menu: ícono 🛒 → lista4. **Configurar IP del backend** en `app/src/main/java/com/precioscerca/api/ApiClient.kt`:

│  • Producto 3       │   - Emulador: `http://10.0.2.2:8000/`

│                     │   - Dispositivo físico: `http://TU-IP-LOCAL:8000/`

└──────────┬──────────┘5. **Build & Run** 📲

           │

           v---

┌─────────────────────┐

│ ListaComprasAct...  │  [LISTA / CHECKLIST]## 📱 Uso de la Aplicación

│                     │

│  Total: $1,234.56   │  - Ver lista completa### 🔍 Búsqueda de productos

│                     │  - ✅ Checkboxes (próximo)

│  ☐ Producto 1       │  - Botón "Finalizar" (próximo)1. Abrir la app **PreciosCerca**

│  ☐ Producto 2       │  - Modo locked al finalizar2. Ver productos aleatorios en la pantalla principal

│  ☐ Producto 3       │3. Escribir término de búsqueda (ej: "leche", "dulce de leche", "aceite de oliva")

│                     │4. Ver resultados ordenados por **precio**

│  [Finalizar Lista]  │5. Presionar **"Agregar a lista"** para guardar productos

└─────────────────────┘6. Ver lista completa con el botón flotante 🛒

```

### 💡 Ejemplos de búsqueda

---

- `leche` → 150+ productos lácteos

## 🧪 Testing- `dulce de leche` → Productos específicos con todas las palabras

- `aceite de oliva` → Búsqueda con palabras compuestas

### Backend- `pan lactal` → Pan de molde comparado

```powershell- `coca cola` → Bebidas gaseosas

# Test scrapers individuales

python backend/test_scraper_directo.py---



# Test palabras compuestas## 🎯 Roadmap

python backend/test_palabras_compuestas.py

### ✅ Completado recientemente

# Test endpoint con filtro

curl "http://localhost:8000/products?query=leche&supermercado=carrefour"- [x] ✅ Agregar supermercado **Día %** (50 productos)

```- [x] ✅ Agregar supermercado **La Reina**

- [x] ✅ Búsqueda con **palabras compuestas**

### Android- [x] ✅ **Imágenes de productos** con Glide

1. Abrir Android Studio- [x] ✅ **Lista de compras** funcional

2. Run → Run 'app'- [x] ✅ Servidor Flask estable con 3 scrapers

3. Probar flujo completo:

   - Click "Empezar Lista"### 📋 Próximo (1-2 semanas)

   - Elegir Carrefour

   - Buscar "leche"- [ ] 🔄 Completar scraper de **La Gallega** con Selenium

   - Agregar producto- [ ] 📍 Búsqueda por **proximidad GPS** (sucursales cercanas)

   - Ver total actualizado- [ ] 💾 **Cache de resultados** para búsquedas frecuentes

   - Ir a lista (ícono carrito)- [ ] 🎨 Mejorar UI con filtros y ordenamiento



---### 🚀 Mediano plazo (1-2 meses)



## 📝 Tecnologías- [ ] Agregar más supermercados (Disco, Jumbo, Coto)

- [ ] Escaneo de códigos de barras

### Android- [ ] Histórico de precios

- **Kotlin** - Lenguaje principal- [ ] Notificaciones de ofertas

- **Material Design 3** - UI components

- **Retrofit 2** - Cliente HTTP REST### 🌟 Largo plazo (3-6 meses)

- **Glide 4.16** - Carga de imágenes

- **RecyclerView** - Listas eficientes- [ ] App iOS

- **CardView** - Cards de productos- [ ] Machine Learning para predicción de precios

- [ ] API pública

### Backend- [ ] Play Store release

- **Flask 3.0** - Framework web Python

- **Requests** - HTTP client para scrapers---

- **BeautifulSoup4** - HTML parsing

- **CORS** - Cross-origin resource sharing## 🎯 Comparación con Competencia



### APIs Utilizadas| Característica | [Pricely.ar](https://pricely.ar) | PreciosCerca | Estado |

- **Carrefour VTEX API** - API oficial pública|----------------|------------|--------------|---------|

- **Día % REST API** - API oficial pública| App Android | ✅ | ✅ | **Logrado** |

- **La Reina HTML** - Web scraping directo| Datos reales | ✅ | ✅ | **Logrado** |

| Supermercados | 10+ | **3 activos** | **En expansión** |

---| Búsqueda compleja | ❓ | ✅ | **Ventaja** |

| Imágenes | ✅ | ✅ | **Logrado** |

## 📜 Versión y Historial| Lista compras | ✅ | ✅ | **Logrado** |

| Código abierto | ❌ | ✅ | **Ventaja** |

**Versión Actual:** 2.0 - Shopping List Focus| Gratis | ✅ | ✅ | **Logrado** |



### Changelog---



#### v2.0 (Actual) - Lista de Compras## 🤝 Contribuir

- ✨ Rediseño completo del flujo de app

- ✨ Selección de supermercado antes de buscar¡Las contribuciones son bienvenidas! 🎉

- ✨ Filtro de productos por supermercado

- ✨ Total acumulado en tiempo real1. **Fork** el proyecto

- 🎨 Nueva UI: MainActivity simplificada2. Crear **feature branch**: `git checkout -b feature/nueva-caracteristica`

- 🎨 SeleccionSuperActivity con cards de marca3. **Commit** cambios: `git commit -m 'Agregar nueva característica'`

- 🎨 BusquedaActivity con total destacado4. **Push** a la branch: `git push origin feature/nueva-caracteristica`

5. Abrir **Pull Request**

#### v1.0 (Anterior) - Comparador de Precios

- 🔍 Búsqueda en múltiples supermercados### 🐛 Reportar bugs

- 📊 Comparación de precios lado a lado

- 📍 Búsqueda por proximidad GPS- Usar [GitHub Issues](https://github.com/Velazquezadrian/PreciosCercaProject/issues)

- 🏪 Vista de sucursales cercanas- Incluir pasos para reproducir el problema

- Especificar versión de Android

**Nota:** El código de v1.0 está disponible en commits anteriores si se necesita volver al comparador de precios.

---

---

## 📄 Licencia

## 🤝 Contribuir

MIT License - Proyecto open source para la comunidad argentina.

Este proyecto está en desarrollo activo. Para contribuir:

Ver archivo `LICENSE` para más detalles.

1. Hacer fork del repositorio

2. Crear branch: `git checkout -b feature/nueva-funcionalidad`---

3. Commit: `git commit -m 'Agregar nueva funcionalidad'`

4. Push: `git push origin feature/nueva-funcionalidad`## 👨‍💻 Contacto

5. Abrir Pull Request

- **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)

---- **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)



## 📄 Licencia---



Este proyecto es de código abierto para fines educativos y de aprendizaje.**⭐ Si te gusta el proyecto, dale una estrella en GitHub!**



---**💰 Desarrollado con ❤️ para ayudar a los argentinos a ahorrar dinero**



## 📞 Soporte**🛒 ¡3 supermercados funcionando, más en camino!**



- **Issues:** [GitHub Issues](https://github.com/tu-usuario/precioscerca/issues)

- **Documentación:** Ver carpeta `docs/`

- **Guía de instalación:** `docs/INSTALLATION.md`**Aplicación completa para comparar precios entre supermercados argentinos con búsqueda por proximidad GPS**

- **Guía de testing:** `docs/TESTING_GUIDE.md`



---

[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)**Aplicación completa para comparar precios entre supermercados argentinos en tiempo real**

**Desarrollado con ❤️ para facilitar las compras del día a día**

[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)

[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)

[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)**Aplicación Android que compara precios de productos en supermercados argentinos usando web scraping en tiempo real****Aplicación completa para comparar precios entre supermercados argentinos en tiempo real**

## ✨ Estado Actual

[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)

### ✅ Completado y funcionando

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)

- **📱 App Android** - APK compilada y funcional con GPS

- **🛒 La Gallega** - 12 sucursales reales en Rosario[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)

- **📍 Búsqueda por proximidad** - Encuentra supermercados cercanos (10-100 km)

- **🗺️ Integración con Google Maps** - Botón "Ver en mapa" para cada sucursal[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)

- **🖥️ Servidor Flask** - API REST estable en puerto 8000

- **🏆 Detección automática** - Muestra el supermercado más cercano al usuario## ✨ Estado Actual - ¡MEJORADO!



### 📊 Características principales[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](backend/)



- **Búsqueda inteligente** por GPS del usuario### ✅ Completado y funcionando

- **Radio configurable** de 10 a 100 km

- **Detección de ciudad** (Buenos Aires, Córdoba, Rosario, Mendoza, etc.)[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)

- **Filtrado automático** - Solo muestra supermercados con sucursales cercanas

- **Ordenamiento por proximidad** - Productos del super más cercano primero- **📱 App Android** - APK compilada y funcional (6.45MB)



## 🚀 Instalación Rápida- **🛒 Carrefour** - 50+ productos reales por búsqueda (API VTEX) ✅[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)



### 📱 Usar la App (5 minutos)- **🏪 Día %** - 50+ productos reales por búsqueda (API REST) ✅ **NUEVO**



1. **Instalar APK:**- **🖥️ Servidor Flask** - API REST estable en puerto 8000

   ```

   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk- **🔄 Arquitectura escalable** - 2 supermercados funcionando

   Tamaño: ~6.5MB

   Requisitos: Android 7.0+## ✨ Estado Actual - ¡FUNCIONANDO!## 📋 Descripción

   ```

### 📊 Resultados actuales

2. **Iniciar servidor:**

   ```bash

   cd backend

   python simple_server.py  # Puerto 8000- **100 productos** por búsqueda (50 de cada supermercado)

   ```

- **2 supermercados** consultados simultáneamente### ✅ Completado y funcionando**PreciosCerca** es un sistema completo que permite a los usuarios argentinos comparar precios de productos entre diferentes supermercados y encontrar las mejores ofertas. El proyecto incluye una API REST robusta y una aplicación móvil Android nativa.

3. **Configurar GPS en tu dispositivo**

   - Dar permisos de ubicación a la app- **Comparación en tiempo real** entre Carrefour y Día %

   - La app detectará automáticamente los supermercados cercanos

- **Ordenamiento automático** por precio (más barato primero)- **📱 App Android** - APK compilada y funcional (6.45MB)

4. **¡Listo!** Busca productos y compara precios



## 🏗️ Arquitectura del Proyecto

### 🔄 Próximos supermercados- **🛒 Carrefour** - 50+ productos reales por búsqueda (API VTEX)### 🎯 Supermercados integrados:

```

PreciosCercaProject/

├── 📱 android/                 # Aplicación Android

│   ├── app/src/main/- **La Reina** - Scraper HTML (necesita actualización)- **🖥️ Servidor Flask** - API REST estable en puerto 8000- 🏪 **La Reina Online** 

│   │   ├── java/com/precioscerca/

│   │   │   ├── MainActivity.kt- **La Gallega** - Scraper con autenticación

│   │   │   ├── ProductListActivity.kt  # Búsqueda con GPS

│   │   │   ├── api/PreciosCercaApi.kt  # Retrofit client- **Disco, Jumbo, Walmart** - En roadmap- **🔄 Arquitectura escalable** - Preparada para más supermercados- 🛒 **Carrefour Argentina**

│   │   │   └── adapters/ProductAdapter.kt

│   │   └── res/

│   │       ├── layout/

│   │       └── menu/menu_product_list.xml  # Radio selector## 🚀 Instalación Rápida- 🏬 **La Gallega**

│   └── build.gradle

├── 🐍 backend/                 # Flask API + Scrapers

│   ├── simple_server.py       # ✅ Servidor principal

│   ├── productos/scrapers/### 📱 Usar la App (5 minutos)### 🔄 En desarrollo

│   │   ├── scraper_carrefour.py  # Usado temporalmente

│   │   ├── scraper_dia.py        # Disponible

│   │   └── sucursales_data.py    # 12 sucursales reales

│   ├── test_ambos.py          # Script de testing1. **Instalar APK:**- **La Reina** - Scraper HTML (estructura lista, necesita debugging)## 🚀 Características principales

│   └── test_sucursales.py     # Prueba de proximidad

├── 📚 docs/   ```

│   ├── PRIVACY_POLICY.md

│   └── INSTALLATION.md   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk- **La Gallega** - Scraper con autenticación

└── README.md

```   Tamaño: 6.45MB



## 📊 API Funcionando   Requisitos: Android 7.0+- **Más supermercados** - Disco, Jumbo, Walmart### ✨ Para usuarios:



### 🌐 Endpoints disponibles   ```



- `GET /products?query=leche` - Buscar productos en todos los supermercados ✅- 🔍 **Búsqueda inteligente** de productos

- `GET /products-cercanos?query=leche&lat=-32.94&lng=-60.64&radio=50` - Buscar solo cercanos ✅

- `GET /sucursal-cercana?supermercado=La+Gallega&lat=-32.94&lng=-60.64` - Sucursal más cercana ✅2. **Iniciar servidor:**

- `GET /sucursales?supermercado=La+Gallega` - Listar sucursales ✅

- `GET /health` - Estado servidor ✅   ```bash## 🚀 Instalación Rápida- 💰 **Comparación de precios** en tiempo real



### 📱 Respuesta de búsqueda cercana (ejemplo)   cd backend



```json   python simple_server.py- 📱 **App móvil** nativa para Android

{

  "query": "leche",   ```

  "lat": -32.9478,

  "lng": -60.6394,### 📱 Usar la App (5 minutos)- 🌐 **Links directos** a productos en supermercados

  "radio_km": 50,

  "ciudad_detectada": "Rosario",3. **¡Listo!** Busca productos y ve precios reales de **Carrefour y Día %**

  "distancia_ciudad_km": 0.5,

  "supermercado_mas_cercano": "La Gallega",- 📊 **Estadísticas** de precios por supermercado

  "distancia_supermercado_mas_cercano_km": 0.34,

  "total_encontrados": 50,## 🏗️ Arquitectura del Proyecto

  "supermercados_consultados": ["La Gallega"],

  "resultados": [1. **Instalar APK:**

    {

      "nombre": "Leche Entera La Serenísima 1L",```

      "precio": 1250.50,

      "supermercado": "La Gallega",PreciosCercaProject/   ```### 🔧 Para desarrolladores:

      "distancia_sucursal_km": 0.34,

      "fecha": "2025-10-30",├── 📱 android/                 # Aplicación Android

      "url": "https://..."

    }│   ├── app/src/main/   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk- 🚀 **API REST** bien documentada

  ]

}│   │   ├── java/com/precioscerca/

```

│   │   │   ├── MainActivity.kt   Tamaño: 6.45MB- 🕷️ **Web scraping** optimizado y paralelo

## 🗺️ Supermercados y Sucursales

│   │   │   ├── ProductListActivity.kt

### La Gallega - Rosario (12 sucursales)

│   │   │   └── api/           # Cliente Retrofit   Requisitos: Android 7.0+- 📊 **Normalización** automática de productos

Datos reales obtenidos de [Tiendeo](https://www.tiendeo.com.ar):

│   │   └── res/               # Recursos UI

- Dorrego 965 (centro)

- Av. Pellegrini 1194│   └── build.gradle   ```- 🗄️ **Base de datos** SQLite con histórico

- Av. Pellegrini 1966

- Catamarca 1498├── 🐍 backend/                 # Flask API + Scrapers

- Urquiza 1145

- Balcarce 248│   ├── simple_server.py       # ✅ Servidor principal- 🎨 **Material Design** en la app móvil

- 9 de Julio 734

- Entre Ríos 2361│   ├── productos/scrapers/

- Avenida Mendoza 255

- Av. Alberdi 465 Bis│   │   ├── scraper_carrefour.py # ✅ Funcionando2. **Iniciar servidor:**

- Córdoba 7605

- Mendoza 7875│   │   ├── scraper_dia.py       # ✅ Funcionando NUEVO



## 🛠️ Para Desarrolladores│   │   ├── scraper_lareina.py   # 🔄 En desarrollo   ```bash## 🏗️ Arquitectura del proyecto



### 🔧 Setup rápido│   │   └── scraper_lagallega.py # 🔄 En desarrollo



```bash│   └── requirements.txt   cd backend

# Clonar

git clone https://github.com/Velazquezadrian/PreciosCercaProject.git├── 📚 docs/



# Backend│   ├── PRIVACY_POLICY.md   C:\PreciosCercaProject\.venv\Scripts\python.exe simple_server.py```

cd backend

python -m venv venv│   └── INSTALLATION.md

source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt└── README.md   ```PreciosCercaProject/

python simple_server.py  # Puerto 8000

```

# Android

cd android├── 🐍 backend/                 # Django REST API

./gradlew assembleDebug  # Genera APK

```## 📊 API Funcionando



### 🧪 Testing3. **¡Listo!** Busca productos y ve precios reales de Carrefour│   ├── productos/              # App principal



```bash### 🌐 Endpoints disponibles

# Probar scrapers

cd backend│   │   ├── scrapers/          # Scrapers por supermercado

python test_ambos.py

- `GET /products?query=leche` - Buscar productos ✅

# Probar sucursales cercanas

python test_sucursales.py- `GET /health` - Estado servidor ✅## 🏗️ Arquitectura Limpia│   │   ├── models.py          # Modelos de datos



# Probar API- `GET /` - Info API ✅

curl "http://localhost:8000/products?query=leche"

curl "http://localhost:8000/products-cercanos?query=leche&lat=-32.9478&lng=-60.6394&radio=50"│   │   └── views.py           # Endpoints de API

```

### 📱 Respuesta real (ejemplo con 2 supermercados)

### 📱 Configurar app Android

```│   ├── manage.py

1. **Abrir Android Studio**

2. **Importar proyecto**: carpeta `android/````json

3. **Sync Gradle** (automático)

4. **Configurar IP del backend** en `ApiClient.kt`:{PreciosCerca/│   └── requirements.txt

   - Emulador: `http://10.0.2.2:8000/`

   - Dispositivo físico: `http://TU-IP-LOCAL:8000/`  "query": "leche",

5. **Build & Run** 📲

  "total_encontrados": 100,├── android/                    # App Android Kotlin├── 📱 android/                 # Aplicación Android

## 📱 Uso de la Aplicación

  "supermercados_consultados": ["Carrefour", "Día %"],

### 🔍 Búsqueda de productos:

  "productos_por_supermercado": {│   └── app/build/outputs/apk/  # ✅ APK funcional│   ├── app/src/main/

1. Abrir la app **PreciosCerca**

2. **Dar permisos de ubicación** cuando los solicite    "Carrefour": 50,

3. Escribir el producto a buscar (ej: "leche", "pan")

4. Ver resultados ordenados por **proximidad** y **precio**    "Día %": 50├── backend/│   │   ├── java/com/precioscerca/

5. Presionar **"Ver en mapa"** para abrir Google Maps con la sucursal más cercana

  },

### 💡 Características GPS:

  "resultados": [│   ├── simple_server.py        # ✅ Servidor principal│   │   │   ├── MainActivity.kt

- **Radio configurable**: 10, 20, 30, 50, 100 km (menú superior derecho)

- **Modo búsqueda**: Alternar entre "cercana" y "general"    {

- **Detección automática**: La app detecta tu ciudad

- **Validación GPS**: Solo Argentina (-55 a -21 lat, -73 a -53 lng)      "nombre": "Tableta chocolatín leche Georgalos 8 g.",│   ├── manage.py              # Django legacy│   │   │   ├── ProductListActivity.kt



## 🎯 Roadmap      "precio": 380.0,



### ✅ Completado recientemente      "supermercado": "Carrefour",│   └── productos/scrapers/     # Módulos scraping│   │   │   ├── api/           # Cliente Retrofit



- [x] Sistema de búsqueda por proximidad GPS      "fecha": "2025-10-30",

- [x] 12 sucursales reales de La Gallega en Rosario

- [x] Detección de supermercado más cercano      "relevancia": 1.0│       ├── base_scraper.py     # Clase base│   │   │   ├── models/        # Modelos de datos

- [x] Integración con Google Maps

- [x] Radio configurable (10-100 km)    },

- [x] Validación de ubicación GPS

- [x] Detección de ciudad (8 ciudades argentinas)    {│       ├── scraper_carrefour.py # ✅ Funcionando│   │   │   └── adapters/      # RecyclerView adapters



### 📋 Próximo (1-2 semanas)      "nombre": "Leche Entera DIA Sachet 1 Lt.",



- [ ] Agregar más supermercados (Carrefour, Día %, etc.)      "precio": 1100.0,│       ├── scraper_lareina.py   # 🔄 En desarrollo│   │   └── res/               # Recursos UI

- [ ] Expandir a más ciudades

- [ ] Mejorar precisión de coordenadas GPS      "supermercado": "Día %",

- [ ] Cache de resultados de búsqueda

      "fecha": "2025-10-30",│       └── scraper_lagallega.py # 🔄 En desarrollo│   └── build.gradle

### 🚀 Mediano plazo (1-2 meses)

      "relevancia": 1.0

- [ ] Histórico de precios

- [ ] Notificaciones de ofertas cercanas    }└── docs/                      # Documentación├── 📚 docs/                   # Documentación

- [ ] Comparación de precios en tiempo real

- [ ] Lista de compras con cálculo de ruta óptima  ]



### 🌟 Largo plazo (3-6 meses)}```│   ├── PRIVACY_POLICY.md      # Política de privacidad



- [ ] App iOS```

- [ ] Machine Learning para predicción de precios

- [ ] API pública│   └── INSTALLATION.md        # Guía de instalación

- [ ] Play Store release

## 🎯 Comparación con Competencia

## 📄 Licencia

## 📊 API Funcionando└── README.md                  # Este archivo

MIT License - Proyecto open source para la comunidad argentina.

| Característica | [Pricely.ar](https://pricely.ar) | PreciosCerca | Estado |

## 👨‍💻 Contacto

|----------------|------------|--------------|---------|```

- **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)

- **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)| App Android | ✅ | ✅ | **Logrado** |



---| Datos reales | ✅ | ✅ | **Logrado** |### 🌐 Endpoints disponibles



**🎉 Sistema funcional con búsqueda por proximidad GPS! Ayudando a argentinos a encontrar los mejores precios cerca de ellos 📍💰**| Supermercados | 10+ | **2 (Carrefour + Día)** | **Mejorado** |


| Código abierto | ❌ | ✅ | **Ventaja** |- `GET /products?query=leche` - Buscar productos ✅## �️ Instalación y configuración

| Escaneo códigos | ✅ | ⏳ | Roadmap |

| Gratis | ✅ | ✅ | **Logrado** |- `GET /health` - Estado servidor ✅



## 🛠️ Para Desarrolladores- `GET /` - Info API ✅### 📋 Prerrequisitos



### 🔧 Setup rápido- **Python 3.8+** para el backend



```bash### 📱 Respuesta real (ejemplo)- **Android Studio** para la app móvil

# Clonar

git clone https://github.com/Velazquezadrian/PreciosCercaProject.git```json- **Git** para clonar el repositorio



# Backend{

cd backend

python simple_server.py  # Puerto 8000  "query": "leche",### 🐍 Backend (Django API)



# Android  "total_encontrados": 50,

cd android

./gradlew assembleDebug  # Genera APK  "supermercados_consultados": ["Carrefour"],1. **Clonar el repositorio:**

```

  "productos_por_supermercado": {"Carrefour": 50},```bash

### 🧪 Testing

  "resultados": [git clone https://github.com/Velazquezadrian/PreciosCercaProject.git

```bash

# Probar API    {cd PreciosCercaProject/backend

curl "http://localhost:8000/products?query=leche"

      "nombre": "Tableta chocolatín leche Georgalos 8 g.",```

# Ver status

curl "http://localhost:8000/health"      "precio": 380.0,



# Test scrapers      "supermercado": "Carrefour",2. **Crear entorno virtual:**

cd backend

python test_ambos.py  # Prueba Carrefour + Día      "fecha": "2025-10-24",```bash

```

      "relevancia": 1.0python -m venv venv

## 📱 Uso de la Aplicación

    },source venv/bin/activate  # En Windows: venv\Scripts\activate

### 🔍 Búsqueda de productos:

    {```

1. Abrir la app **PreciosCerca**

2. Escribir el producto a buscar (ej: "leche", "pan", "arroz")      "nombre": "Tableta dulce de leche Vauquita 25 g.",

3. Presionar **"Buscar precios"**

4. Ver resultados comparativos de **Carrefour y Día %**      "precio": 615.0,3. **Instalar dependencias:**



### 💡 Ejemplos de búsqueda:      "supermercado": "Carrefour",```bash



- `leche` → 100 productos de 2 supermercados      "fecha": "2025-10-24", pip install -r requirements.txt

- `pan lactal` → Pan de molde comparado

- `arroz largo fino` → Arroz específico      "relevancia": 1.0```

- `coca cola` → Bebidas gaseosas

    }

## 🎯 Roadmap

  ]4. **Configurar base de datos:**

### ⚡ Completado recientemente

}```bash

- [x] ✅ Agregar supermercado **Día %** (50 productos)

- [x] ✅ Búsqueda combinada en 2 supermercados (100 productos)```python manage.py migrate

- [x] ✅ Servidor Flask estable con múltiples scrapers

```

### 📋 Próximo (1-2 semanas)

## 🎯 Comparación con Competencia

- [ ] Agregar **Disco** scraper

- [ ] Mejorar interfaz Android con filtros5. **Ejecutar servidor:**

- [ ] Cache de resultados para búsquedas frecuentes

| Característica | [Pricely.ar](https://pricely.ar) | PreciosCerca | Estado |```bash

### 🚀 Mediano plazo (1-2 meses)

|----------------|------------|--------------|---------|python manage.py runserver

- [ ] Jumbo, Walmart scrapers

- [ ] Escaneo códigos de barras| App Android | ✅ | ✅ | **Logrado** |```

- [ ] Histórico de precios

- [ ] Notificaciones ofertas| Datos reales | ✅ | ✅ | **Logrado** |



### 🌟 Largo plazo (3-6 meses)| Supermercados | 10+ | 1 (Carrefour) | En expansión |🎉 **API disponible en**: `http://localhost:8000/api/products?query=leche`



- [ ] App iOS| Código abierto | ❌ | ✅ | **Ventaja** |

- [ ] Machine Learning predicción precios

- [ ] API pública| Escaneo códigos | ✅ | ⏳ | Roadmap |### 📱 App Android

- [ ] Play Store release

| Gratis | ✅ | ✅ | **Logrado** |

## 📄 Licencia

1. **Abrir Android Studio**

MIT License - Proyecto open source para la comunidad argentina.

## 🛠️ Para Desarrolladores2. **Importar proyecto**: `android/` folder

## 👨‍💻 Contacto

3. **Sync Gradle** (automático)

- **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)

- **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)### 🔧 Setup rápido4. **Configurar IP del backend** en `ApiClient.kt`:



---```bash   - Emulador: `http://10.0.2.2:8000/`



**🎉 ¡App funcional con 2 supermercados! Ayudando a argentinos a ahorrar dinero 💰**# Clonar   - Dispositivo físico: `http://TU-IP-LOCAL:8000/`


git clone https://github.com/Velazquezadrian/PreciosCercaProject.git5. **Build & Run** 📲



# Backend## 📱 Uso de la aplicación

cd backend

python simple_server.py  # Puerto 8000### 🔍 Búsqueda de productos:

1. Abrir la app **PreciosCerca**

# Android2. Escribir el producto a buscar (ej: "leche", "pan", "arroz")

cd android3. Presionar **"Buscar precios"**

./gradlew assembleDebug  # Genera APK4. Ver resultados comparativos por supermercado

```

### 💡 Ejemplos de búsqueda:

### 🧪 Testing- `leche` → Productos lácteos

```bash- `pan lactal` → Pan de molde

# Probar API- `arroz largo fino` → Arroz específico

curl "http://localhost:8000/products?query=leche"- `coca cola` → Bebidas gaseosas



# Ver status## 🔧 API Reference

curl "http://localhost:8000/health"

```### 🌐 Endpoint principal



## 🗂️ Archivos Limpiados**GET** `/api/products?query={producto}`



Se eliminaron archivos de prueba innecesarios:**Parámetros:**

- ❌ `test_*.py` (múltiples archivos de testing)- `query` (string, requerido): Término de búsqueda

- ❌ `final_test.py` 

- ❌ `server_real_scrapers.py` (duplicado)**Respuesta de ejemplo:**

- ✅ Mantenido: `simple_server.py` (servidor principal)```json

- ✅ Mantenido: `manage.py` (Django legacy){

  "query": "leche",

## 🎯 Roadmap  "total_encontrados": 15,

  "supermercados_consultados": ["La Reina", "Carrefour", "La Gallega"],

### ⚡ Próximo (1-2 semanas)  "productos_por_supermercado": {

- [ ] Arreglar scraper La Reina (debugging)    "La Reina": 6,

- [ ] Arreglar scraper La Gallega (autenticación)    "Carrefour": 5,

- [ ] Mejorar interfaz Android    "La Gallega": 4

  },

### 🚀 Mediano plazo (1-2 meses)  "resultados": [

- [ ] Disco, Jumbo, Walmart scrapers    {

- [ ] Escaneo códigos de barras      "nombre": "Leche La Serenísima Entera 1L",

- [ ] Histórico de precios      "precio": 850.99,

- [ ] Notificaciones ofertas      "supermercado": "La Reina",

      "fecha": "2025-10-22T15:30:00",

### 🌟 Largo plazo (3-6 meses)      "relevancia": 0.95

- [ ] App iOS    }

- [ ] Machine Learning predicción precios  ]

- [ ] API pública}

- [ ] Play Store release```



## 📄 Licencia## 🎯 Roadmap completado



MIT License - Proyecto open source para la comunidad argentina.- ✅ **Bloque 1**: Modelo de datos + API básica  

- ✅ **Bloque 2**: Scraper La Reina + integración DB

## 👨‍💻 Contacto- ✅ **Bloque 3**: Scrapers múltiples + normalización

- ✅ **Bloque 4**: App Android MVP funcional

- **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)- ✅ **Bloque 5**: Branding y preparación para Play Store

- **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)

## 🧪 Testing

---

### 🔍 Probar API:

**🎉 ¡App funcional que ya compite con Pricely.ar! Ayudando a argentinos a ahorrar dinero 💰**```bash
curl "http://localhost:8000/api/products?query=arroz"
```

### 📱 Probar App:
1. Ejecutar backend en `localhost:8000`
2. Abrir app en emulador/dispositivo
3. Buscar productos y verificar resultados

## 🚀 Deployment

### 🌐 Backend (Heroku/DigitalOcean):
```bash
# Configurar variables de entorno
export DEBUG=False
export ALLOWED_HOSTS=tu-dominio.com
python manage.py collectstatic
gunicorn precioscerca_backend.wsgi
```

### 📱 Android (Play Store):
1. Generar APK firmado en Android Studio
2. Subir a Google Play Console
3. Completar store listing con screenshots

## 🤝 Contribuir al proyecto

¡Las contribuciones son bienvenidas! 🎉

1. **Fork** el proyecto
2. Crear **feature branch**: `git checkout -b feature/nueva-caracteristica`
3. **Commit** cambios: `git commit -m 'Agregar nueva característica'`
4. **Push** a la branch: `git push origin feature/nueva-caracteristica`
5. Abrir **Pull Request**

### 🐛 Reportar bugs:
- Usar [GitHub Issues](https://github.com/Velazquezadrian/PreciosCercaProject/issues)
- Incluir pasos para reproducir el problema
- Especificar dispositivo/versión Android

## 📄 Licencia

Este proyecto está bajo la **MIT License**. Ver `LICENSE` para más detalles.

## 📞 Contacto

- 👨‍💻 **Desarrollador**: Adrián Velázquez  
- 📧 **Email**: [tu-email@ejemplo.com]
- 🐙 **GitHub**: [@Velazquezadrian](https://github.com/Velazquezadrian)
- 🔗 **Proyecto**: [PreciosCercaProject](https://github.com/Velazquezadrian/PreciosCercaProject)

## 🙏 Agradecimientos

- 🛒 Supermercados por mantener datos públicos accesibles
- 📱 Google por Android SDK y Material Design
- 🐍 Django community por el framework robusto
- ☕ Café, mucho café ☕

---

**⭐ Si te gusta el proyecto, dale una estrella en GitHub!**

**💰 Desarrollado con ❤️ para ayudar a los argentinos a ahorrar dinero**

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver archivo `LICENSE` para detalles.

## 🐛 Issues y Support

Para reportar bugs o solicitar features, usa las [GitHub Issues](https://github.com/usuario/PreciosCercaProject/issues).

---

**Desarrollado con ❤️ para ayudar a encontrar los mejores precios**