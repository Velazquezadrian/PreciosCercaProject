# 🛒 Precios Cerca - Comparador de Precios

**Aplicación completa para comparar precios de supermercados en Argentina**

## 📋 Descripción

Sistema completo que incluye API REST y aplicación móvil para comparar precios entre supermercados (La Reina, Carrefour, La Gallega).

## 🏗️ Estructura del Proyecto

```
PreciosCercaProject/
├── backend/          # Django REST API
├── android/          # Aplicación Android  
├── docs/             # Documentación
└── README.md         # Este archivo
```

## 🚀 Componentes

### Backend (Django REST API)
- **Ubicación**: `./backend/`
- **Tecnologías**: Django 4.2, Python 3.13, SQLite
- **Funcionalidades**:
  - API REST endpoint `/products?query=...`
  - Scrapers para La Reina, Carrefour, La Gallega
  - Normalización de productos y precios
  - Base de datos con histórico de precios

### Android App
- **Ubicación**: `./android/`
- **Tecnologías**: Kotlin, Retrofit, Material Design
- **Funcionalidades**:
  - Búsqueda de productos
  - Lista de resultados con precios
  - Botones "Ver en web" y "Ver en mapa"
  - Diseño responsive para móviles

## 🛠️ Instalación y Uso

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Android
```bash
cd android
./gradlew assembleDebug
```

## 📱 Demo

- **API Endpoint**: `http://localhost:8000/products?query=arroz`
- **Supermercados**: La Reina, Carrefour, La Gallega
- **Respuesta**: JSON con productos normalizados

## 🎯 Roadmap

- [x] **Bloque 1**: Modelo de datos + API básica
- [x] **Bloque 2**: Scraper La Reina + integración DB  
- [x] **Bloque 3**: Scrapers múltiples + normalización
- [ ] **Bloque 4**: App Android + Play Store
- [ ] **Bloque 5**: Optimizaciones y features avanzadas

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