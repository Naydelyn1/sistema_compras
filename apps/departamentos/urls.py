from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_departamentos, name='lista_departamentos'),
    path('nuevo/', views.crear_departamento, name='crear_departamento'),
]
