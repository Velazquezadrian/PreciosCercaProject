from django.db import models

# MODELOS - Tablas de la base de datos

class Supermercado(models.Model):
    # Información básica del supermercado
    nombre = models.CharField(max_length=100)  # "La Reina", "Carrefour"
    url_sitio = models.URLField()  # "https://www.lareinaonline.com.ar"
    activo = models.BooleanField(default=True)  # Si está disponible para scraping
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # Información del producto
    nombre = models.CharField(max_length=200)  # "Leche La Serenísima 1L"
    categoria = models.CharField(max_length=100)  # "Lácteos", "Bebidas" 
    
    def __str__(self):
        return self.nombre

class Precio(models.Model):
    # Conexiones con otras tablas
    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE)  # Cuál supermercado
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Cuál producto
    
    # Información del precio
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # $1234.56
    url_producto = models.URLField()  # Link directo al producto
    fecha = models.DateTimeField(auto_now_add=True)  # Cuándo se guardó
    
    def __str__(self):
        return f"{self.producto.nombre} - ${self.precio}"