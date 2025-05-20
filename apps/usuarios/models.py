
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.username})'

# Create your models here.
