# Precarga del Catálogo de La Gallega

## ¿Por qué precargar?

La Gallega tiene **miles de productos** distribuidos en **136 categorías**. Buscarlos en tiempo real cada vez es LENTO (10-15 segundos por búsqueda).

Con la **precarga**, descargamos TODO el catálogo UNA SOLA VEZ y lo guardamos en caché. Después las búsquedas son **instantáneas** (< 100ms).

## Cómo precargar

### Paso 1: Ejecutar el script de precarga

```powershell
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe precargar_lagallega.py
```

**Tiempo estimado:** 10-15 minutos (solo se hace UNA VEZ)

El script:
- Recorre las 136 categorías de La Gallega
- Extrae TODOS los productos (nombre, precio, URL de imagen)
- Guarda todo en `productos_cache.json` (solo URLs, NO descarga imágenes)
- Muestra progreso en tiempo real

### Paso 2: Reiniciar el servidor

Una vez completada la precarga, reinicia el servidor Flask:

```powershell
cd C:\PreciosCercaProject\backend
& C:\PreciosCercaProject\.venv\Scripts\python.exe simple_server.py
```

### Paso 3: Probar búsqueda instantánea

```powershell
curl "http://192.168.100.3:8000/products?query=pan&supermercado=lagallega"
```

Debería retornar **TODOS** los productos con "pan" en **menos de 1 segundo**.

## ¿Qué se guarda en el caché?

```json
{
  "lagallega": {
    "Pan lactal Bimbo x 650g": {
      "categoria": "03000000",
      "precio": 1250.50,
      "imagen_url": "https://www.lagallega.com.ar/imagenes/...",
      "url": "https://www.lagallega.com.ar/producto.asp?...",
      "last_update": "2025-11-25T18:00:00"
    },
    "Bizcochos de pan x kg": {
      ...
    }
  }
}
```

**SOLO se guardan URLs**, NO se descargan imágenes (Android + Glide lo hace eficientemente).

## Ventajas

✅ **Búsquedas instantáneas** (< 100ms vs 10-15 segundos)
✅ **Todos los productos** disponibles siempre
✅ **Sin límites** de productos por búsqueda
✅ **No satura** el servidor de La Gallega con requests
✅ **Funciona offline** una vez precargado

## Cuándo re-precargar

- Cada 7-15 días para actualizar precios
- Cuando La Gallega agregue productos nuevos
- Si el caché se corrompe o borra

## Tamaño del caché

- Archivo: `productos_cache.json`
- Tamaño estimado: 2-5 MB (solo texto/URLs)
- Productos: ~2000-5000 productos

## Búsqueda con palabra completa

El sistema usa búsqueda inteligente:
- `"pan"` → encuentra: "pan lactal", "bizcochos de pan", "pan rallado"
- `"pan"` → NO encuentra: "emPANada", "camPANa"
- `"dulce de leche"` → encuentra productos con "dulce" Y "leche"
