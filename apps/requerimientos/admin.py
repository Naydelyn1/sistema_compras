from django.contrib import admin
from .models import Requerimiento, DetalleRequerimiento, HistorialAprobacion

admin.site.register(Requerimiento)
admin.site.register(DetalleRequerimiento)
admin.site.register(HistorialAprobacion)

# Register your models here.
