from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True, default='SIN-CODIGO')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Create your models here.
