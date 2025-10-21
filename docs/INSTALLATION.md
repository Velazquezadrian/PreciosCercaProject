# 🔧 Guía de Instalación

## Backend (Django API)

### Requisitos
- Python 3.11+
- pip (gestor de paquetes Python)

### Pasos de instalación

1. **Navegar al directorio backend**
   ```bash
   cd backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   ```

3. **Activar entorno virtual**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Instalar dependencias**
   ```bash
   pip install django djangorestframework requests beautifulsoup4 lxml
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```

7. **Probar API**
   - Abrir: `http://127.0.0.1:8000/products?query=arroz`

## Android App

### Requisitos
- Android Studio Arctic Fox+
- JDK 11+
- Android SDK 24+ (Android 7.0)

### Pasos de instalación

1. **Abrir Android Studio**
2. **Import Project**: Seleccionar carpeta `android/`
3. **Sync Project**: Gradle sync automático
4. **Run**: Ejecutar en emulador o dispositivo

## 🧪 Testing

### Backend
```bash
cd backend
python manage.py test
```

### API Manual Testing
```bash
# Probar búsquedas
curl "http://127.0.0.1:8000/products?query=cafe"
curl "http://127.0.0.1:8000/products?query=leche"
curl "http://127.0.0.1:8000/products?query=arroz"
```

## 🚀 Deployment

### Backend - Heroku/Railway
1. Configurar `requirements.txt`
2. Agregar `Procfile`
3. Deploy con Git

### Android - Google Play Store
1. Generar APK firmado
2. Crear cuenta Google Play Developer ($25)
3. Subir APK y configurar store listing