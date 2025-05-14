from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('nuevo/', views.crear_orden, name='crear_orden'),
    path('<int:orden_id>/agregar-detalle/', views.agregar_detalle_orden, name='agregar_detalle_orden'),
    path('<int:orden_id>/detalle/', views.detalle_orden, name='detalle_orden'),
    path('<int:orden_id>/cambiar-estado/<str:nuevo_estado>/', views.cambiar_estado_orden, name='cambiar_estado_orden'),
    path('<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
    path('detalle/eliminar/<int:detalle_id>/', views.eliminar_detalle_orden, name='eliminar_detalle_orden'),
    path('<int:orden_id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),





]
