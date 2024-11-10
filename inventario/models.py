from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    cantidad_minima = models.IntegerField(default=5)  # Cantidad mínima de inventario
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    # Función para verificar si el inventario está bajo
    def inventario_bajo(self):
        return self.cantidad < self.cantidad_minima
# Create your models here.
