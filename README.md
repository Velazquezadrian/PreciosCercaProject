# 🛒 PreciosCerca - Comparador de Precios Android# 🛒 PreciosCerca - Comparador de Precios de Supermercados



**Aplicación Android que compara precios de productos en supermercados argentinos usando web scraping en tiempo real****Aplicación completa para comparar precios entre supermercados argentinos en tiempo real**



[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)

[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](backend/)[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](backend/)

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)

[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)



## ✨ Estado Actual - ¡FUNCIONANDO!## 📋 Descripción



### ✅ Completado y funcionando**PreciosCerca** es un sistema completo que permite a los usuarios argentinos comparar precios de productos entre diferentes supermercados y encontrar las mejores ofertas. El proyecto incluye una API REST robusta y una aplicación móvil Android nativa.

- **📱 App Android** - APK compilada y funcional (6.45MB)

- **🛒 Carrefour** - 50+ productos reales por búsqueda (API VTEX)### 🎯 Supermercados integrados:

- **🖥️ Servidor Flask** - API REST estable en puerto 8000- 🏪 **La Reina Online** 

- **🔄 Arquitectura escalable** - Preparada para más supermercados- 🛒 **Carrefour Argentina**

- 🏬 **La Gallega**

### 🔄 En desarrollo

- **La Reina** - Scraper HTML (estructura lista, necesita debugging)## 🚀 Características principales

- **La Gallega** - Scraper con autenticación

- **Más supermercados** - Disco, Jumbo, Walmart### ✨ Para usuarios:

- 🔍 **Búsqueda inteligente** de productos

## 🚀 Instalación Rápida- 💰 **Comparación de precios** en tiempo real

- 📱 **App móvil** nativa para Android

### 📱 Usar la App (5 minutos)- 🌐 **Links directos** a productos en supermercados

- 📊 **Estadísticas** de precios por supermercado

1. **Instalar APK:**

   ```### 🔧 Para desarrolladores:

   Ubicación: android/app/build/outputs/apk/debug/app-debug.apk- 🚀 **API REST** bien documentada

   Tamaño: 6.45MB- 🕷️ **Web scraping** optimizado y paralelo

   Requisitos: Android 7.0+- 📊 **Normalización** automática de productos

   ```- 🗄️ **Base de datos** SQLite con histórico

- 🎨 **Material Design** en la app móvil

2. **Iniciar servidor:**

   ```bash## 🏗️ Arquitectura del proyecto

   cd backend

   C:\PreciosCercaProject\.venv\Scripts\python.exe simple_server.py```

   ```PreciosCercaProject/

├── 🐍 backend/                 # Django REST API

3. **¡Listo!** Busca productos y ve precios reales de Carrefour│   ├── productos/              # App principal

│   │   ├── scrapers/          # Scrapers por supermercado

## 🏗️ Arquitectura Limpia│   │   ├── models.py          # Modelos de datos

│   │   └── views.py           # Endpoints de API

```│   ├── manage.py

PreciosCerca/│   └── requirements.txt

├── android/                    # App Android Kotlin├── 📱 android/                 # Aplicación Android

│   └── app/build/outputs/apk/  # ✅ APK funcional│   ├── app/src/main/

├── backend/│   │   ├── java/com/precioscerca/

│   ├── simple_server.py        # ✅ Servidor principal│   │   │   ├── MainActivity.kt

│   ├── manage.py              # Django legacy│   │   │   ├── ProductListActivity.kt

│   └── productos/scrapers/     # Módulos scraping│   │   │   ├── api/           # Cliente Retrofit

│       ├── base_scraper.py     # Clase base│   │   │   ├── models/        # Modelos de datos

│       ├── scraper_carrefour.py # ✅ Funcionando│   │   │   └── adapters/      # RecyclerView adapters

│       ├── scraper_lareina.py   # 🔄 En desarrollo│   │   └── res/               # Recursos UI

│       └── scraper_lagallega.py # 🔄 En desarrollo│   └── build.gradle

└── docs/                      # Documentación├── 📚 docs/                   # Documentación

```│   ├── PRIVACY_POLICY.md      # Política de privacidad

│   └── INSTALLATION.md        # Guía de instalación

## 📊 API Funcionando└── README.md                  # Este archivo

```

### 🌐 Endpoints disponibles

- `GET /products?query=leche` - Buscar productos ✅## �️ Instalación y configuración

- `GET /health` - Estado servidor ✅

- `GET /` - Info API ✅### 📋 Prerrequisitos

- **Python 3.8+** para el backend

### 📱 Respuesta real (ejemplo)- **Android Studio** para la app móvil

```json- **Git** para clonar el repositorio

{

  "query": "leche",### 🐍 Backend (Django API)

  "total_encontrados": 50,

  "supermercados_consultados": ["Carrefour"],1. **Clonar el repositorio:**

  "productos_por_supermercado": {"Carrefour": 50},```bash

  "resultados": [git clone https://github.com/Velazquezadrian/PreciosCercaProject.git

    {cd PreciosCercaProject/backend

      "nombre": "Tableta chocolatín leche Georgalos 8 g.",```

      "precio": 380.0,

      "supermercado": "Carrefour",2. **Crear entorno virtual:**

      "fecha": "2025-10-24",```bash

      "relevancia": 1.0python -m venv venv

    },source venv/bin/activate  # En Windows: venv\Scripts\activate

    {```

      "nombre": "Tableta dulce de leche Vauquita 25 g.",

      "precio": 615.0,3. **Instalar dependencias:**

      "supermercado": "Carrefour",```bash

      "fecha": "2025-10-24", pip install -r requirements.txt

      "relevancia": 1.0```

    }

  ]4. **Configurar base de datos:**

}```bash

```python manage.py migrate

```

## 🎯 Comparación con Competencia

5. **Ejecutar servidor:**

| Característica | [Pricely.ar](https://pricely.ar) | PreciosCerca | Estado |```bash

|----------------|------------|--------------|---------|python manage.py runserver

| App Android | ✅ | ✅ | **Logrado** |```

| Datos reales | ✅ | ✅ | **Logrado** |

| Supermercados | 10+ | 1 (Carrefour) | En expansión |🎉 **API disponible en**: `http://localhost:8000/api/products?query=leche`

| Código abierto | ❌ | ✅ | **Ventaja** |

| Escaneo códigos | ✅ | ⏳ | Roadmap |### 📱 App Android

| Gratis | ✅ | ✅ | **Logrado** |

1. **Abrir Android Studio**

## 🛠️ Para Desarrolladores2. **Importar proyecto**: `android/` folder

3. **Sync Gradle** (automático)

### 🔧 Setup rápido4. **Configurar IP del backend** en `ApiClient.kt`:

```bash   - Emulador: `http://10.0.2.2:8000/`

# Clonar   - Dispositivo físico: `http://TU-IP-LOCAL:8000/`

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