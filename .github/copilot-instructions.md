# Mi Lista de Precios - Copilot Context

## App Overview
**Purpose**: Android shopping list app for Argentine supermarkets. Users create lists for ONE supermarket at a time, search products, see real-time total, and check off items while shopping.

**Core Flow**:
1. Choose mode: "Mi Lista de Compra" (save list) or "Buscar Producto" (browse only)
2. Select supermarket: Carrefour, Día %, or La Reina
3. Search products (multi-word: "dulce de leche", "aceite de oliva")
4. Add to list with image, price, supermercado
5. See running total: `sum(precio * cantidad)`
6. "Terminar Lista" → tap products to mark as bought (grayscale effect)
7. Share list via WhatsApp (✅ bought / ⬜ pending format)

**Key Differentiator**: Focus on ONE supermarket per list (not price comparison). User knows exactly what they'll spend before going to the store.

## Stack
- **Backend**: Flask 3.0 + Python 3.8+ (port 8000)
- **Android**: Kotlin + Material3 + Gradle 8.12 (minSdk 24, targetSdk 34)
- **Build**: Android Studio JBR, no Gradle daemon issues
hora si 
## Architecture

### Backend (Flask API)
```
backend/
├── simple_server.py          # Flask app, 5 endpoints
├── lista_compras.py          # In-memory list state
└── productos/
    ├── services.py           # buscar_productos_similares(query, productos)
    └── scrapers/
        ├── base_scraper.py   # Abstract class
        ├── scraper_carrefour.py  # VTEX API
        ├── scraper_dia.py        # REST API
        └── scraper_lareina.py    # BeautifulSoup HTML
```

**Key patterns:**
- Scrapers return: `[{nombre, precio, supermercado, imagen, url}]`
- Multi-word search: API uses first word → Python filters all words (avoid 400 errors)
- services.py: `palabras_query.issubset(palabras_encontradas)` logic

### Android (Kotlin)
```
app/src/main/java/com/precioscerca/
├── MainActivity.kt               # 2 buttons: LISTA/CONSULTA modes
├── SeleccionSuperActivity.kt    # Pass MODO+SUPERMERCADO
├── BusquedaActivity.kt           # Search + add to list
├── MiListaActivity.kt            # RecyclerView + total
├── ListaTerminadaActivity.kt    # Grayscale tap + share
├── api/
│   ├── ApiClient.kt              # Retrofit base URL
│   └── PreciosCercaApi.kt        # @GET @POST @DELETE
├── adapters/
│   ├── ProductAdapter.kt         # Search results
│   ├── MiListaAdapter.kt         # 60x60 images
│   └── ListaTerminadaAdapter.kt  # ColorMatrixColorFilter
└── models/
    └── ProductoEnLista.kt        # @Parcelize data class
```

**Key patterns:**
- Glide for images (placeholder, error, diskCache)
- Retrofit: `ApiClient.api.endpoint()` + `enqueue(Callback)`
- FileProvider for sharing: `${applicationId}.fileprovider`

## API Contract

### GET /products
```kotlin
// Query: ?query=leche&supermercado=carrefour (optional filter)
// Response: {query, total_encontrados, supermercados_consultados, productos_por_supermercado, resultados[]}
```

### POST /lista-compras/agregar
```json
{"nombre":"str", "cantidad":int, "precio":float, "supermercado":"str", "imagen":"url"}
```

### DELETE /lista-compras/eliminar
```json
{"nombre":"str"}
```

### GET /lista-compras
```kotlin
// Response: {items[], total_items:int}
```

## UI/UX Design

### Color Palette
```xml
Primary: #2196F3 (Material Blue)
Primary Dark: #1976D2
Primary Light: #64B5F6
Accent: #FF9800 (Material Orange)
Accent Dark: #F57C00

Background: #F5F5F5 (Gray Light)
Text Primary: #424242 (Gray Dark)
Text Secondary: #9E9E9E (Gray Medium)

Precio Color: #4CAF50 (Green)
Supermercado BG: #E3F2FD (Light Blue)
Descuento: #F44336 (Red)
```

### Typography
- **Headers**: 28sp bold, white on primary background
- **Subtitles**: 14sp, #CCFFFFFF (80% white)
- **Body**: 16sp, gray_dark (#424242)
- **Button Text**: 18-24sp bold, white
- **Icons (emoji)**: 48sp

### Screen Layouts

#### MainActivity (Pantalla Principal)
**Structure:**
- Header: Primary blue background (#2196F3), 20dp padding, 4dp elevation
  - Title: "PreciosCerca" (28sp bold white)
  - Subtitle: "Compará precios y ahorrá" (14sp, #CCFFFFFF)
- Body: Gray background (#F5F5F5), 24dp padding, vertical center

**Buttons:**
- 2 CardViews igual tamaño (layout_weight=1)
- Corner radius: 16dp, Elevation: 8dp
- Spacing: 16dp between cards
- Ripple effect: `?attr/selectableItemBackground`

1. **btnMiLista** (Top):
   - Background: @color/primary (#2196F3)
   - Icon: 📝 (48sp)
   - Title: "Mi Lista de Compra" (24sp bold white)
   - Subtitle: "Creá tu lista y guardala" (14sp, #CCFFFFFF)

2. **btnConsultaPrecios** (Bottom):h
   - Background: @color/accent (#FF9800)
   - Icon: 🔍 (48sp)
   - Title: "Buscar Producto" (24sp bold white)
   - Subtitle: "Solo consultá sin guardar" (14sp, #CCFFFFFF)

#### SeleccionSuperActivity (Elegir Supermercado)
**Structure:**
- Background: #F5F5F5, 16dp padding
- Title: "Elegí tu supermercado" (24sp bold, center, 24dp bottom margin)

**Cards (3 total):**
- Height: 100dp, Full width
- Corner radius: 16dp, Elevation: 6dp
- Spacing: 16dp bottom margin
- Horizontal layout, center vertical

1. **cardCarrefour**:
   - Background: #0054A4 (Carrefour blue)
   - Text: "🛒 Carrefour" (24sp bold white)

2. **cardDia**:
   - Background: #D32F2F (Día red)
   - Text: "🛒 Día %" (24sp bold white)

3. **cardLaReina**:
   - Background: #388E3C (La Reina green)
   - Text: "🛒 La Reina" (24sp bold white)

#### BusquedaActivity (Búsqueda de Productos)
**Structure:**
- Background: #F5F5F5

**Search Bar:**
- Background: @color/primary, 16dp padding, 8dp elevation
- Horizontal layout, center vertical
- TextInputEditText: White background, 52dp height, 16dp padding
- MaterialButton: @color/accent background, 52dp height, white text "Buscar"

**Total Bar:**
- Background: @color/supermercado_bg (#E3F2FD)
- 16dp padding, horizontal layout
- Left: "Total de tu lista:" (16sp, gray_dark)
- Right: "$0.00" (24sp bold, @color/precio_color #4CAF50)

**Content:**
- tvEstado: Center, "Buscá productos para agregar a tu lista" (16sp, gray_medium)
- recyclerProductos: Full width, 8dp top/bottom padding
- progressBar: Center, hidden by default

#### MiListaActivity (Mi Lista de Compra)
**Structure:**
- Background: @color/gray_light (#F5F5F5)

**Header:**
- Background: @color/primary (#2196F3)
- 20dp padding, 8dp elevation
- Horizontal layout, center vertical
- Left: "Total de tu lista:" (18sp bold white)
- Right: "$0.00" (28sp bold white) [tvTotalLista]

**Content:**
- tvEstadoLista: Center, "Tu lista está vacía" (16sp gray_medium, hidden by default)
- recyclerLista: 16dp padding all sides
- btnTerminarLista: Full width, 64dp height, 16dp margin
  - Text: "Terminar Lista" (18sp bold white)
  - Background: @color/accent (#FF9800)
  - Corner radius: 12dp
  - Hidden by default (visibility="gone")

#### ListaTerminadaActivity (Lista Finalizada)
**Structure:**
- Background: @color/gray_light (#F5F5F5)

**Header:**
- Background: @color/primary (#2196F3)
- 20dp padding, 8dp elevation
- Vertical layout
- Top: "Tocá los productos para marcarlos como comprados" (14sp, @color/supermercado_bg)
- Bottom horizontal:
  - Left: "Total:" (18sp bold white)
  - Right: "$0.00" (28sp bold white) [tvTotalTerminado]

**Content:**
- recyclerListaTerminada: 16dp padding all sides
- btnCompartir: Full width, 64dp height, 16dp margin
  - Text: "📤 Compartir Lista" (18sp bold white)
  - Background: @color/precio_color (#4CAF50)
  - Corner radius: 12dp

### Product Items
**Adapter Layouts:**
- `item_producto.xml`: Search results (BusquedaActivity)
- `item_producto_lista.xml`: Shopping list items (MiListaActivity)
- `item_producto_terminado.xml`: Finished list with grayscale toggle (ListaTerminadaActivity)

**Common Specs:**
- CardView: 12dp corner radius, 4dp elevation
- Product images: 60x60dp via Glide
- Price: Bold, @color/precio_color (#4CAF50)
- Supermercado badge: @color/supermercado_bg background

### Grayscale Effect (ListaTerminadaActivity)
```kotlin
// Apply to ImageView when producto.comprado = true
val matrix = ColorMatrix()
matrix.setSaturation(0f) // Remove color
imageView.colorFilter = ColorMatrixColorFilter(matrix)
```

### Icon System
- App uses emoji icons (no drawable resources needed):
  - 📝 (Lista), 🔍 (Buscar), 🛒 (Supermercado), 📤 (Compartir)
- Launcher icon: `ic_launcher.png` / `ic_launcher_round.png` in `mipmap/` folders

## Common Issues

### Backend
- **Multi-word search**: Use `services.buscar_productos_similares(query, productos)` after scraping
- **Scrapers keys**: `'carrefour'`, `'dia'`, `'lareina'` (lowercase in dict)
- **CORS**: Flask-CORS enabled for Android localhost

### Android
- **IP config**: Emulator=`10.0.2.2:8000`, Device=`192.168.x.x:8000`
- **Parcelize**: Requires `kotlin-parcelize` plugin in build.gradle
- **FileProvider**: `meta-data` in AndroidManifest + `file_paths.xml`
- **Glide**: Always `.diskCacheStrategy(DiskCacheStrategy.ALL)`
- **Java version**: Use Android Studio JBR, set `JAVA_HOME` for gradlew

## Build Commands
```bash
# Backend
python backend/simple_server.py

# Android (PowerShell)
Push-Location android
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
.\gradlew.bat assembleDebug
Pop-Location
```

## Data Flow
1. User searches "dulce de leche" in BusquedaActivity
2. Android: `query = "dulce de leche"`, `supermercado = "carrefour"`
3. Backend: `/products?query=dulce%20de%20leche&supermercado=carrefour`
4. Scraper uses "dulce" (first word) to avoid API 400
5. `buscar_productos_similares()` filters: ["dulce", "de", "leche"] all present
6. Android renders 50 products, adds to lista with precio+imagen
7. MiListaActivity shows total: `sum(producto.precio * producto.cantidad)`
8. ListaTerminadaActivity: tap → `comprado=true` → grayscale

## Testing
```bash
# Backend multi-word
python backend/test_palabras_compuestas.py

# API health
curl http://localhost:8000/health
```

## State Management
- Backend: `lista_compras_global` in-memory (no DB)
- Android: Parcelable intents, no ViewModel/SavedState yet

## Dependencies
- Backend: Flask, requests, beautifulsoup4
- Android: Retrofit 2.9.0, Glide 4.16.0, Material3 1.2.0

## Critical Files
- `backend/simple_server.py`: All endpoints
- `backend/productos/services.py`: Filter logic
- `android/app/src/main/java/com/precioscerca/api/ApiClient.kt`: Base URL
- `android/app/build.gradle`: Plugins, dependencies

## Known Limitations
- No database persistence (lista cleared on server restart)
- No auth/users
- La Reina scraper unstable (HTML changes)
- GPS/sucursales endpoints return 501 (not implemented)
