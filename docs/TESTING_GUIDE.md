# 🧪 Guía de Testing - PreciosCerca

## 📋 Checklist de pruebas completas

### 🐍 **Backend - Django API**

#### ✅ Pruebas básicas:
```bash
cd backend
python manage.py test
```

#### 🔍 Pruebas de scrapers:
```bash
# Probar endpoint principal
curl "http://localhost:8000/api/products?query=arroz"

# Verificar respuesta JSON válida
curl "http://localhost:8000/api/products?query=leche" | jq .

# Probar con productos específicos
curl "http://localhost:8000/api/products?query=coca%20cola"
```

#### 🕷️ Verificar scrapers individuales:
```bash
# La Reina
python manage.py shell
>>> from productos.scrapers.scraper_lareina import ScraperLaReina
>>> scraper = ScraperLaReina()
>>> productos = scraper.buscar_productos("leche")
>>> print(f"Encontrados: {len(productos)} productos")

# Carrefour  
>>> from productos.scrapers.scraper_carrefour import ScraperCarrefour
>>> scraper = ScraperCarrefour()
>>> productos = scraper.buscar_productos("pan")
>>> print(f"Encontrados: {len(productos)} productos")

# La Gallega
>>> from productos.scrapers.scraper_lagallega import ScraperLaGallega
>>> scraper = ScraperLaGallega()  
>>> productos = scraper.buscar_productos("arroz")
>>> print(f"Encontrados: {len(productos)} productos")
```

### 📱 **App Android**

#### ⚡ Testing funcional:

**1. Pantalla principal (MainActivity):**
- [ ] Logo se muestra correctamente
- [ ] Campo de búsqueda acepta texto
- [ ] Botón "Buscar precios" responde
- [ ] Validación de texto vacío funciona
- [ ] Indicador de carga aparece/desaparece

**2. Lista de productos (ProductListActivity):**
- [ ] Navegación desde MainActivity funciona
- [ ] Título muestra query correctamente
- [ ] Lista de productos se carga
- [ ] Cards de productos muestran información completa
- [ ] Precios se formatean correctamente ($X,XXX.XX)
- [ ] Fechas se muestran en formato amigable
- [ ] Click en producto abre navegador web
- [ ] Botón volver funciona

**3. Conectividad:**
- [ ] App maneja error de conexión graciosamente
- [ ] Timeout de requests funciona (30 segundos)
- [ ] Mensajes de error son claros para el usuario

#### 🔄 Testing de flujo completo:

**Escenario 1: Búsqueda exitosa**
1. Abrir app
2. Escribir "leche"  
3. Presionar "Buscar precios"
4. Verificar que aparecen resultados de múltiples supermercados
5. Click en un producto
6. Verificar que abre navegador con sitio del supermercado

**Escenario 2: Búsqueda sin resultados**
1. Escribir "productoinexistente123"
2. Presionar buscar
3. Verificar mensaje "No se encontraron productos"

**Escenario 3: Error de conexión**
1. Desconectar WiFi/datos móviles
2. Intentar búsqueda
3. Verificar mensaje de error de conexión

#### 📏 Testing de UI/UX:

- [ ] Diseño responsive en diferentes tamaños de pantalla
- [ ] Colores del tema se aplican correctamente
- [ ] Textos legibles y bien contrastados
- [ ] Animaciones fluidas
- [ ] Touch targets suficientemente grandes (>48dp)

### 🌐 **Testing de integración completa**

#### 🔄 Flujo end-to-end:
```bash
# Terminal 1: Iniciar backend
cd backend
python manage.py runserver

# Terminal 2: Probar API manualmente
curl "http://localhost:8000/api/products?query=arroz" 

# Verificar respuesta:
# - query: "arroz"
# - total_encontrados: > 0
# - supermercados_consultados: ["La Reina", "Carrefour", "La Gallega"]
# - resultados: array con productos
```

#### 📱 Emulador/dispositivo físico:
1. **Configurar IP correcta** en `ApiClient.kt`
2. **Build & Run** la app
3. **Probar búsquedas reales** con productos comunes:
   - "leche" → Debería encontrar ~10-20 productos
   - "pan" → Productos de panadería  
   - "arroz" → Diferentes tipos de arroz
   - "coca cola" → Bebidas gaseosas

### ⚡ **Optimización de rendimiento**

#### 🐍 Backend:
- [ ] Requests paralelos a scrapers (ThreadPoolExecutor)
- [ ] Timeout de 30 segundos por scraper
- [ ] Cache de resultados (opcional)
- [ ] Logs de errores configurados

#### 📱 Android:
- [ ] Imágenes vectoriales en lugar de PNG cuando sea posible
- [ ] RecyclerView con ViewHolder pattern
- [ ] Requests asíncronos con Retrofit
- [ ] Manejo apropiado de memoria

### 🐛 **Casos edge comunes**

#### 🔍 Búsquedas problemáticas:
- Texto muy corto: "a"
- Texto muy largo: "producto con nombre extremadamente largo..."  
- Caracteres especiales: "café", "niño"
- Números: "coca cola 2.25l"
- Sin conexión a internet

#### 🛒 Productos específicos a probar:
- **Lácteos**: "leche", "yogur", "queso"
- **Panadería**: "pan", "facturas", "medialunas" 
- **Bebidas**: "agua", "gaseosa", "jugo"
- **Limpieza**: "detergente", "lavandina", "jabón"
- **Carnes**: "asado", "pollo", "pescado"

### 📊 **Métricas a verificar**

#### ⏱️ Performance:
- Tiempo de respuesta API: < 10 segundos promedio
- Tiempo de carga app: < 3 segundos
- Uso de memoria: < 100MB
- Tamaño APK: < 20MB

#### 📈 Funcionalidad:
- % de búsquedas exitosas: > 80%
- Productos encontrados promedio: > 5 por búsqueda
- Uptime de scrapers: > 90%

---

## ✅ **Checklist final de release**

### 🔄 Pre-release:
- [ ] Todos los tests pasan
- [ ] API responde correctamente
- [ ] App funciona en emulador
- [ ] App funciona en dispositivo físico  
- [ ] No hay crashes evidentes
- [ ] Documentación actualizada

### 🚀 Ready for launch:
- [ ] APK firmado generado
- [ ] Screenshots tomados
- [ ] Descripción de Play Store lista
- [ ] Política de privacidad publicada
- [ ] README actualizado con versión final

**🎉 ¡PreciosCerca listo para el mundo!**