# Sistema de Caché Inteligente para Productos

## 🎯 Objetivo

Acelerar las búsquedas de productos usando un sistema de caché local que:
1. **Guarda productos** en archivo JSON con categorías
2. **Descarga y optimiza imágenes** a formato WebP (liviano)
3. **Búsqueda instantánea** cuando el producto ya está en caché
4. **Actualización automática** al buscar productos nuevos

## 📂 Estructura de Archivos

```
backend/
├── cache_manager.py              # Gestor del caché (clase principal)
├── productos_cache.json          # Caché de productos (JSON)
├── imagenes_productos/           # Imágenes optimizadas (WebP)
│   ├── lagallega_pan_lactal_a1b2c3d4.webp
│   ├── lagallega_leche_serenisima_e5f6g7h8.webp
│   └── ...
└── precargar_cache.py            # Script de precarga (opcional)
```

## 🔄 Flujo de Trabajo

### Búsqueda CON Caché (instantánea)

```
Usuario busca "pan" en La Gallega
    ↓
1. cache_manager.buscar_producto('lagallega', 'pan')
    ↓
2. Encuentra 15 productos en productos_cache.json
    ↓
3. Retorna instantáneamente con imágenes locales
    ⚡ Tiempo: < 100ms
```

### Búsqueda SIN Caché (primera vez)

```
Usuario busca "aceite de oliva" en La Gallega
    ↓
1. cache_manager.buscar_producto() → 0 resultados
    ↓
2. scraper_lagallega.buscar_productos() → busca en web
    ↓
3. Por cada producto encontrado:
   - Descarga imagen original
   - Redimensiona a máx 300x300px
   - Convierte a WebP (75% calidad)
   - Guarda en imagenes_productos/
    ↓
4. Guarda productos en productos_cache.json
    ↓
5. Retorna resultados
    🕐 Tiempo: 5-10 segundos (solo primera vez)
```

### Próxima Búsqueda (con caché)

```
Usuario busca "aceite" de nuevo
    ↓
1. Encuentra en caché inmediatamente
    ↓
2. Retorna con imágenes locales optimizadas
    ⚡ Tiempo: < 100ms
```

## 📝 Estructura del Caché JSON

```json
{
  "last_update": "2025-11-25T10:30:00",
  "productos": {
    "lagallega": {
      "pan lactal bimbo": {
        "categoria": "02000000",
        "precio": 1250.50,
        "imagen_local": "imagenes_productos/lagallega_pan_lactal_bimbo_abc123.webp",
        "url": "https://www.lagallega.com.ar/...",
        "last_update": "2025-11-25T10:30:00"
      },
      "leche serenisima": {
        "categoria": "03000000",
        "precio": 950.00,
        "imagen_local": "imagenes_productos/lagallega_leche_serenisima_def456.webp",
        "url": "https://www.lagallega.com.ar/...",
        "last_update": "2025-11-25T10:31:00"
      }
    },
    "lareina": {},
    "carrefour": {},
    "dia": {}
  }
}
```

## 🖼️ Optimización de Imágenes

### ANTES (imagen original)
- Formato: JPG/PNG
- Tamaño: 800x800px
- Peso: 150-300 KB
- Tiempo descarga: 2-3 segundos

### DESPUÉS (imagen optimizada)
- Formato: **WebP** (formato moderno de Google)
- Tamaño: **máx 300x300px**
- Peso: **10-30 KB** (90% más liviano!)
- Tiempo descarga: < 0.5 segundos

### Ventajas del WebP
- Compresión superior a JPG/PNG (30-50% más liviano)
- Calidad visual similar
- Soporte en todos los navegadores modernos y Android
- Carga más rápida en la app

## 🚀 Uso del Sistema

### 1. Iniciar servidor con caché activado

```bash
cd backend
python simple_server.py
```

El servidor automáticamente:
- Carga el caché existente de `productos_cache.json`
- Usa búsqueda en caché cuando es posible
- Actualiza el caché con nuevas búsquedas
- Sirve imágenes optimizadas en `/imagenes/<archivo>.webp`

### 2. (Opcional) Pre-cargar productos populares

```bash
python precargar_cache.py
```

Esto busca y guarda en caché 16 productos populares:
- pan, leche, aceite, arroz, fideos
- yerba, café, azúcar, harina, manteca
- dulce de leche, queso, galletitas, mayonesa
- tomate, gaseosa

**⚠️ Advertencia**: Este script puede tardar 10-20 minutos porque busca cada producto en la web.

### 3. Verificar estadísticas del caché

```bash
curl http://localhost:8000/cache/stats
```

Retorna:
```json
{
  "status": "success",
  "cache": {
    "lagallega": {
      "total_productos": 245,
      "con_imagen": 238
    },
    "lareina": {
      "total_productos": 0,
      "con_imagen": 0
    }
  },
  "last_update": "2025-11-25T10:30:00"
}
```

## 🔧 API de cache_manager

### Buscar en caché

```python
from cache_manager import cache_manager

# Buscar productos
resultados = cache_manager.buscar_producto('lagallega', 'pan lactal')

# Retorna:
[
  {
    'nombre': 'Pan Lactal Bimbo',
    'categoria': '02000000',
    'precio': 1250.50,
    'imagen_local': 'imagenes_productos/lagallega_pan_lactal_abc.webp',
    'url': 'https://...'
  }
]
```

### Agregar producto al caché

```python
cache_manager.agregar_producto(
    supermercado='lagallega',
    nombre='Leche Serenisima',
    categoria='03000000',
    precio=950.00,
    url='https://www.lagallega.com.ar/...',
    imagen_url='https://www.lagallega.com.ar/imagenes/producto.jpg'
)

# Esto automáticamente:
# 1. Descarga la imagen
# 2. La optimiza a WebP
# 3. La guarda en imagenes_productos/
# 4. Actualiza productos_cache.json
```

### Obtener estadísticas

```python
stats = cache_manager.obtener_estadisticas()
print(stats)
# {
#   'lagallega': {'total_productos': 245, 'con_imagen': 238},
#   'lareina': {'total_productos': 0, 'con_imagen': 0}
# }
```

## 🎨 Manejo de Productos Sin Imagen

Si un producto no tiene imagen o falla la descarga:
1. El campo `imagen_local` queda en `None`
2. El endpoint `/imagenes/<archivo>` retorna `logo_sin_imagen.png`
3. La app muestra un placeholder genérico

## ⚡ Performance Esperado

### Primera búsqueda (sin caché)
- Tiempo: 5-10 segundos
- Downloads: 20-50 imágenes optimizadas
- Escritura: productos_cache.json actualizado

### Búsquedas posteriores (con caché)
- Tiempo: **< 100ms** ⚡
- Downloads: 0 (todo local)
- Lectura: productos_cache.json en memoria

### Ahorro de datos
- Imagen original: ~200 KB
- Imagen WebP: ~20 KB
- **Ahorro: 90%** 🎉

## 🔄 Actualización del Caché

El caché se actualiza automáticamente:
- Cuando se busca un producto que no está en caché
- Se puede forzar borrar `productos_cache.json` para refrescar
- No hay expiración automática (manual por ahora)

## 📊 Monitoreo

Archivos a revisar:
- `productos_cache.json` - Cuántos productos hay
- `imagenes_productos/` - Cuántas imágenes descargadas
- Consola del servidor - Logs de caché hits/misses

## 🛠️ Troubleshooting

### Problema: "ModuleNotFoundError: PIL"
```bash
pip install Pillow
```

### Problema: Imágenes no se cargan en Android
- Verificar URL: `http://192.168.100.3:8000/imagenes/archivo.webp`
- Verificar que existe en `imagenes_productos/`
- Ver logs del servidor Flask

### Problema: Caché no se guarda
- Verificar permisos de escritura en `backend/`
- Ver logs en consola al guardar

### Problema: Imágenes muy pesadas
- Ajustar calidad en `cache_manager.py` línea 92:
  ```python
  img.save(ruta_local, 'WEBP', quality=75, optimize=True)
  # Reducir quality a 60 para archivos aún más livianos
  ```

## 🎯 Próximas Mejoras

- [ ] Expiración automática del caché (ej: 7 días)
- [ ] Endpoint para refrescar caché de un producto
- [ ] Precarga en background al iniciar servidor
- [ ] Compresión aún mayor para redes lentas
- [ ] Cache también para Carrefour, Día, La Reina
