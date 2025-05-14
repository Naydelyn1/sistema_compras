from django.db import models

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=200, unique=True)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    persona_contacto = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.razon_social} - RUC: {self.ruc}'
