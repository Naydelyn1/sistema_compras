from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_requerimientos, name='lista_requerimientos'),  # Listar requerimientos
    path('nuevo/', views.crear_requerimiento, name='crear_requerimiento'),  # Crear nuevo requerimiento
    path('<int:requerimiento_id>/editar/', views.editar_requerimiento, name='editar_requerimiento'),  # Editar requerimiento
    path('<int:requerimiento_id>/eliminar/', views.eliminar_requerimiento, name='eliminar_requerimiento'),  # Eliminar requerimiento
    path('<int:requerimiento_id>/agregar-detalle/', views.agregar_detalle_requerimiento, name='agregar_detalle_requerimiento'),  # Agregar detalle

    path('solicitante/', views.lista_requerimientos_solicitante, name='lista_requerimientos_solicitante'),
    path('solicitante/nuevo/', views.crear_requerimiento_solicitante, name='crear_requerimiento_solicitante'),
    path('solicitante/<int:requerimiento_id>/eliminar/', views.eliminar_requerimiento_solicitante, name='eliminar_requerimiento_solicitante'),
    path('solicitante/<int:requerimiento_id>/editar/', views.editar_requerimiento_solicitante, name='editar_requerimiento_solicitante'),
    
    # Cambiar la URL para que sea más consistente y funcione desde cualquier vista
    path('api/productos-por-categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
]