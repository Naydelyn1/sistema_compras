from django.urls import path
from . import views

urlpatterns = [
    path('productos_por_categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
]
