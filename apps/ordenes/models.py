from django.db import models
from apps.requerimientos.models import Requerimiento
from apps.proveedores.models import Proveedor
from apps.productos.models import Producto

class OrdenCompra(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, related_name='ordenes')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha_emision = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='pendiente')

    def __str__(self):
        return f'Orden {self.id} - {self.proveedor.razon_social}'


class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en Orden {self.orden.id}'


# Create your models here.
