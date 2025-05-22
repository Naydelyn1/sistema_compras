from django.db import models
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from apps.productos.models import Producto
from django import forms



class Requerimiento(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    ESTADO_CHOICES = [
        ('sin_ejecutar', 'Sin Ejecutar'),
        ('emitida', 'Emitida'),
        ('recibida', 'Recibida'),
        ('completa', 'Completa'),
        ('pendiente', 'Pendiente'),  # Puedes mantener el que ya tenías si quieres
    ]

    nombre = models.CharField(max_length=150, null=False, blank=False)

    solicitante = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='requerimientos')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='requerimientos')
    fecha = models.DateField(auto_now_add=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f'Requerimiento {self.id} - {self.nombre}'



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


class RequerimientoSolicitanteForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['prioridad']  # Solo el campo que puede elegir el solicitante

    # Opcional: Si quieres mostrar prioridad con select personalizado
    prioridad = forms.ChoiceField(
        choices=Requerimiento.PRIORIDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
# Create your models here.
# Agregar este modelo al final de tu models.py si no lo tienes

class HistorialAprobacion(models.Model):
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=[
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ])
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Historial de Aprobación'
        verbose_name_plural = 'Historial de Aprobaciones'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Requerimiento #{self.requerimiento.id} - {self.accion} - {self.usuario}"