# Nuevos Supermercados para Agregar

## Estado Actual
✅ **4 supermercados activos:**
- Carrefour (VTEX API) - ~500 productos en caché
- Día % (VTEX API) - ~500 productos en caché
- La Reina (HTML Scraping) - ~2,600 productos en caché
- La Gallega (HTML Scraping con 136 categorías) - ~5,000 productos en caché

## Candidatos para Expansión

### 🟢 Alta Prioridad (APIs Disponibles)

#### 1. **Coto Digital**
- **Website**: https://www.cotodigital3.com.ar/
- **Tecnología**: VTEX API (similar a Carrefour/Día)
- **Productos estimados**: 8,000+
- **Cobertura**: Buenos Aires, GBA, interior
- **Dificultad**: ⭐⭐ (Baja - API estructurada)
- **Ventajas**: 
  - Gran variedad de productos
  - Precios muy competitivos
  - Buena cobertura nacional
- **Notas**: Requiere API key o scraping de API pública

#### 2. **Disco / Jumbo** (Grupo Cencosud)
- **Website**: https://www.disco.com.ar / https://www.jumbo.com.ar
- **Tecnología**: VTEX API compartida
- **Productos estimados**: 12,000+ (ambas cadenas)
- **Cobertura**: CABA, GBA, provincias
- **Dificultad**: ⭐⭐ (Baja - API VTEX)
- **Ventajas**:
  - Dos marcas en una sola integración
  - Amplio catálogo premium (Jumbo) y económico (Disco)
  - Muy buena API
- **Notas**: Mismo backend VTEX, diferentes precios

#### 3. **Walmart Argentina** (rebranded como Changomás)
- **Website**: https://www.walmart.com.ar
- **Tecnología**: API REST propia
- **Productos estimados**: 10,000+
- **Cobertura**: Buenos Aires, Rosario, Córdoba, Mendoza
- **Dificultad**: ⭐⭐⭐ (Media - API con autenticación)
- **Ventajas**:
  - Marca internacional
  - Buenos precios en electrónica y juguetes
  - Integración con tienda física
- **Notas**: Migró a Changomás en algunas sucursales

### 🟡 Media Prioridad (HTML Scraping Estable)

#### 4. **Vea Digital**
- **Website**: https://www.veadigital.com.ar/
- **Tecnología**: HTML con categorías navegables
- **Productos estimados**: 5,000+
- **Cobertura**: Interior de Argentina (fuerte en Córdoba, Santa Fe)
- **Dificultad**: ⭐⭐⭐ (Media - HTML estructurado)
- **Ventajas**:
  - Buena presencia en provincias
  - Precios económicos
  - Estructura HTML predecible
- **Notas**: Similar a La Gallega, requiere categorías hardcodeadas

#### 5. **Farmacity** (sección almacén)
- **Website**: https://www.farmacity.com/alimentos-y-bebidas
- **Tecnología**: API REST moderna
- **Productos estimados**: 3,000 (alimentos/bebidas)
- **Cobertura**: CABA, GBA
- **Dificultad**: ⭐⭐ (Baja - API de farmacia digital)
- **Ventajas**:
  - Productos de almacén, snacks, bebidas
  - Entrega rápida (1-2 horas)
  - API muy estable
- **Notas**: No es supermercado completo, pero útil para productos específicos

### 🔴 Baja Prioridad (Difícil o Regional)

#### 6. **Toledo** (Grupo Coto)
- **Website**: https://www.supermercadostoledo.com.ar/
- **Tecnología**: HTML básico
- **Productos estimados**: 2,000+
- **Cobertura**: Solo Buenos Aires zona oeste
- **Dificultad**: ⭐⭐⭐⭐ (Alta - HTML desorganizado)
- **Ventajas**:
  - Precios bajos
  - Presencia local fuerte
- **Notas**: Cobertura muy limitada, HTML inconsistente

#### 7. **Makro** (mayorista)
- **Website**: https://www.makro.com.ar/
- **Tecnología**: SAP Hybris API
- **Productos estimados**: 15,000+
- **Cobertura**: Mayorista (requiere CUIT)
- **Dificultad**: ⭐⭐⭐⭐ (Alta - requiere cuenta empresarial)
- **Ventajas**:
  - Precios mayoristas muy bajos
  - Gran variedad
- **Desventajas**:
  - Requiere registrarse como empresa
  - No para consumidor final
- **Notas**: Útil solo si agregamos modo "compras mayoristas"

## Plan de Implementación

### Fase 1 (Inmediato - 1 semana)
1. ✅ Precarga automática diaria (8 AM) - **COMPLETADO**
2. ✅ Notificación de mantenimiento en app - **COMPLETADO**
3. **Agregar Coto Digital** (VTEX API - reutilizar código de Carrefour)
4. **Agregar Disco/Jumbo** (VTEX API - misma estructura)

### Fase 2 (Mediano plazo - 2-3 semanas)
5. **Agregar Vea Digital** (HTML scraping - similar a La Gallega)
6. **Agregar Walmart/Changomás** (API REST propia)
7. Optimizar imágenes (CDN o compresión)

### Fase 3 (Futuro - 1-2 meses)
8. **Agregar Farmacity** (sección alimentos)
9. Sistema de favoritos por supermercado
10. Comparador de precios entre supermercados
11. Notificaciones de ofertas/descuentos

## Consideraciones Técnicas

### Backend (Python/Flask)
- **Patrón actual**: `backend/productos/scrapers/scraper_NOMBRE.py`
- **Base class**: `BaseScraper` con métodos abstractos
- **Cache**: JSON con precarga automática diaria
- **API**: Endpoint `/products` con filtro por supermercado

### Android (Kotlin)
- **API Interface**: `PreciosCercaApi.kt` - agregar casos en `@Query("supermercado")`
- **Selección**: `SeleccionSuperActivity.kt` - agregar CardView por cada nuevo super
- **Colors**: Agregar color corporativo en `colors.xml`
- **Imágenes**: Logos en `drawable/` (opcional, actualmente usa emojis 🛒)

### Limitaciones
- **Railway timeout**: 120s máximo (por eso usamos precarga)
- **Scrapers HTML**: Frágiles a cambios de estructura web
- **APIs sin documentación**: Reverse engineering necesario
- **Rate limiting**: Algunos supermercados limitan requests/minuto

## Métricas Objetivo

### Cobertura
- **Actual**: 4 supermercados
- **Meta Fase 1**: 7 supermercados (agregar Coto + Disco/Jumbo + Vea)
- **Meta Fase 2**: 9 supermercados (agregar Walmart + Farmacity)
- **Meta largo plazo**: 10-12 supermercados principales de Argentina

### Catálogo
- **Actual**: ~8,500 productos en caché
- **Meta Fase 1**: ~30,000 productos (con Coto, Disco, Jumbo, Vea)
- **Meta Fase 2**: ~45,000 productos (agregar Walmart)

### Performance
- **Búsqueda actual**: <500ms (desde caché)
- **Precarga diaria**: <45 minutos para todos los supers
- **Paginación**: 30 productos/página, scroll infinito

## Preguntas para el Usuario

1. **Prioridad geográfica**: ¿CABA/GBA o también provincias?
2. **Tipos de productos**: ¿Solo almacén o también farmacia, electrónica, etc.?
3. **Modo mayorista**: ¿Agregar Makro (requiere CUIT)?
4. **Preferencias de marca**: ¿Algún supermercado específico que uses más?
5. **Funcionalidades nuevas**: ¿Comparador de precios entre supers? ¿Ofertas/descuentos?

---

**Última actualización**: Diciembre 2024
**Estado del sistema**: ✅ Precarga automática activa, 4 supermercados operativos
