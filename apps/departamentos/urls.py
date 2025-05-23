from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_departamentos, name='lista_departamentos'),
    path('nuevo/', views.crear_departamento, name='crear_departamento'),
    path('editar/<int:departamento_id>/', views.editar_departamento, name='editar_departamento'),
    path('eliminar/<int:departamento_id>/', views.eliminar_departamento, name='eliminar_departamento'),
    path('toggle/<int:departamento_id>/', views.toggle_departamento, name='toggle_departamento'),
]