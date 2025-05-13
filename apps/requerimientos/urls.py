from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_requerimientos, name='lista_requerimientos'),
    path('nuevo/', views.crear_requerimiento, name='crear_requerimiento'),
    path('<int:requerimiento_id>/agregar-detalle/', views.agregar_detalle_requerimiento, name='agregar_detalle_requerimiento'),
   
]
