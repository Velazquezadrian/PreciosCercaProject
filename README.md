# 🛒 PreciosCerca - Comparador de Precios de Supermercados

**Aplicación completa para comparar precios entre supermercados argentinos en tiempo real**

[![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)](android/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](backend/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](backend/)
[![Kotlin](https://img.shields.io/badge/Kotlin-0095D5?style=flat&logo=kotlin&logoColor=white)](android/)

## 📋 Descripción

**PreciosCerca** es un sistema completo que permite a los usuarios argentinos comparar precios de productos entre diferentes supermercados y encontrar las mejores ofertas. El proyecto incluye una API REST robusta y una aplicación móvil Android nativa.

### 🎯 Supermercados integrados:
- 🏪 **La Reina Online** 
- 🛒 **Carrefour Argentina**
- 🏬 **La Gallega**

## 🚀 Características principales

### ✨ Para usuarios:
- 🔍 **Búsqueda inteligente** de productos
- 💰 **Comparación de precios** en tiempo real
- 📱 **App móvil** nativa para Android
- 🌐 **Links directos** a productos en supermercados
- 📊 **Estadísticas** de precios por supermercado

### 🔧 Para desarrolladores:
- 🚀 **API REST** bien documentada
- 🕷️ **Web scraping** optimizado y paralelo
- 📊 **Normalización** automática de productos
- 🗄️ **Base de datos** SQLite con histórico
- 🎨 **Material Design** en la app móvil

## 🏗️ Arquitectura del proyecto

```
PreciosCercaProject/
├── 🐍 backend/                 # Django REST API
│   ├── productos/              # App principal
│   │   ├── scrapers/          # Scrapers por supermercado
│   │   ├── models.py          # Modelos de datos
│   │   └── views.py           # Endpoints de API
│   ├── manage.py
│   └── requirements.txt
├── 📱 android/                 # Aplicación Android
│   ├── app/src/main/
│   │   ├── java/com/precioscerca/
│   │   │   ├── MainActivity.kt
│   │   │   ├── ProductListActivity.kt
│   │   │   ├── api/           # Cliente Retrofit
│   │   │   ├── models/        # Modelos de datos
│   │   │   └── adapters/      # RecyclerView adapters
│   │   └── res/               # Recursos UI
│   └── build.gradle
├── 📚 docs/                   # Documentación
│   ├── PRIVACY_POLICY.md      # Política de privacidad
│   └── INSTALLATION.md        # Guía de instalación
└── README.md                  # Este archivo
```

## �️ Instalación y configuración

### 📋 Prerrequisitos
- **Python 3.8+** para el backend
- **Android Studio** para la app móvil
- **Git** para clonar el repositorio

### 🐍 Backend (Django API)

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Velazquezadrian/PreciosCercaProject.git
cd PreciosCercaProject/backend
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
```bash
python manage.py migrate
```

5. **Ejecutar servidor:**
```bash
python manage.py runserver
```

🎉 **API disponible en**: `http://localhost:8000/api/products?query=leche`

### 📱 App Android

1. **Abrir Android Studio**
2. **Importar proyecto**: `android/` folder
3. **Sync Gradle** (automático)
4. **Configurar IP del backend** en `ApiClient.kt`:
   - Emulador: `http://10.0.2.2:8000/`
   - Dispositivo físico: `http://TU-IP-LOCAL:8000/`
5. **Build & Run** 📲

## 📱 Uso de la aplicación

### 🔍 Búsqueda de productos:
1. Abrir la app **PreciosCerca**
2. Escribir el producto a buscar (ej: "leche", "pan", "arroz")
3. Presionar **"Buscar precios"**
4. Ver resultados comparativos por supermercado

### 💡 Ejemplos de búsqueda:
- `leche` → Productos lácteos
- `pan lactal` → Pan de molde
- `arroz largo fino` → Arroz específico
- `coca cola` → Bebidas gaseosas

## 🔧 API Reference

### 🌐 Endpoint principal

**GET** `/api/products?query={producto}`

**Parámetros:**
- `query` (string, requerido): Término de búsqueda

**Respuesta de ejemplo:**
```json
{
  "query": "leche",
  "total_encontrados": 15,
  "supermercados_consultados": ["La Reina", "Carrefour", "La Gallega"],
  "productos_por_supermercado": {
    "La Reina": 6,
    "Carrefour": 5,
    "La Gallega": 4
  },
  "resultados": [
    {
      "nombre": "Leche La Serenísima Entera 1L",
      "precio": 850.99,
      "supermercado": "La Reina",
      "fecha": "2025-10-22T15:30:00",
      "relevancia": 0.95
    }
  ]
}
```

## 🎯 Roadmap completado

- ✅ **Bloque 1**: Modelo de datos + API básica  
- ✅ **Bloque 2**: Scraper La Reina + integración DB
- ✅ **Bloque 3**: Scrapers múltiples + normalización
- ✅ **Bloque 4**: App Android MVP funcional
- ✅ **Bloque 5**: Branding y preparación para Play Store

## 🧪 Testing

### 🔍 Probar API:
```bash
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