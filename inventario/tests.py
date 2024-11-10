from django.test import TestCase
from django.urls import reverse
from .models import Producto

# Pruebas Unitarias
class ProductoTestCase(TestCase):
    def test_registro_producto(self):
        """Verifica que el registro de un producto funcione correctamente"""
        producto = Producto.objects.create(
            nombre="Producto 1",
            cantidad=10,
            precio=100.00,
            descripcion="Descripción del producto",
        )
        # Verifica que el producto se ha registrado correctamente
        self.assertEqual(producto.nombre, "Producto 1")
        self.assertEqual(producto.cantidad, 10)
        self.assertEqual(producto.precio, 100.00)

    def test_actualizar_stock(self):
        """Verifica que el stock de un producto se pueda actualizar"""
        producto = Producto.objects.create(
            nombre="Producto 2",
            cantidad=5,
            precio=50.00,
            descripcion="Producto con stock bajo",
        )
        # Actualiza el stock
        producto.cantidad += 10
        producto.save()

        # Verifica que la cantidad ha sido actualizada correctamente
        self.assertEqual(producto.cantidad, 15)




# Create your tests here.
