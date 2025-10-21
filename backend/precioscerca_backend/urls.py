from django.contrib import admin
from django.urls import path, include  # Agregar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),  # Conectar URLs de productos
]
