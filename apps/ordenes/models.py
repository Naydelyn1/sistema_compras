from django.db import models
from apps.requerimientos.models import Requerimiento
from apps.proveedores.models import Proveedor
from apps.usuarios.models import Usuario
from apps.productos.models import Producto

class OrdenCompra(models.Model):
    ESTADOS_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('recibida', 'Recibida'),
        ('completada', 'Completada'),
    ]

    codigo = models.CharField(max_length=50, default='ORD-001')
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.PROTECT, related_name='ordenes')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    usuario_emisor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='borrador')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    condiciones_pago = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Orden {self.codigo} - {self.proveedor.razon_social}'

class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ debe ser un campo, no una propiedad

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en Orden {self.orden.codigo}'


    
    def calcular_total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())
