from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('nuevo/', views.crear_orden, name='crear_orden'),
    path('<int:orden_id>/agregar-detalle/', views.agregar_detalle_orden, name='agregar_detalle_orden'),
]
