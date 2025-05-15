from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_requerimientos, name='lista_requerimientos'),  # Listar requerimientos
    path('nuevo/', views.crear_requerimiento, name='crear_requerimiento'),  # Crear nuevo requerimiento
    path('<int:requerimiento_id>/editar/', views.editar_requerimiento, name='editar_requerimiento'),  # Editar requerimiento
    path('<int:requerimiento_id>/eliminar/', views.eliminar_requerimiento, name='eliminar_requerimiento'),  # Eliminar requerimiento
    path('<int:requerimiento_id>/agregar-detalle/', views.agregar_detalle_requerimiento, name='agregar_detalle_requerimiento'),  # Agregar detalle
]
