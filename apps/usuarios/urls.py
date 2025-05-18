from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('nuevo/', views.crear_usuario, name='crear_usuario'),
    path('<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario')

]
