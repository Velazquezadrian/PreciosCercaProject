from django.urls import path
from . import views

urlpatterns = [
    path('products', views.buscar_productos, name='buscar_productos'),
]
