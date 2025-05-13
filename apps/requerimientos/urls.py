from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_requerimientos, name='lista_requerimientos'),
   
]
