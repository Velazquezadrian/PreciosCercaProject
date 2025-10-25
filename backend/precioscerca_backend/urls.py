from django.contrib import admin
from django.urls import path, include  # Agregar include
from productos.views import buscar_productos  # Importar vista directamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', buscar_productos, name='buscar_productos'),  # URL directa
]
