from django.db import models
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from apps.productos.models import Producto



class Requerimiento(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    solicitante = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='requerimientos')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='requerimientos')
    fecha = models.DateField(auto_now_add=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=50, default='pendiente')

    def __str__(self):
        return f'Requerimiento {self.id} - {self.solicitante}'


class DetalleRequerimiento(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} para {self.requerimiento}'
    
    

class HistorialAprobacion(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name='historial_aprobaciones')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    accion = models.CharField(max_length=50)  # Ej: aprobado, rechazado
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.requerimiento} - {self.accion} por {self.usuario}'



# Create your models here.
