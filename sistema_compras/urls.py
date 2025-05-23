"""
URL configuration for sistema_compras project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home 
from django.urls import include, path



urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuarios.urls')),
    path('departamentos/', include('apps.departamentos.urls')),
    path('requerimientos/', include('apps.requerimientos.urls')),
    path('proveedores/', include('apps.proveedores.urls')),
    path('productos/', include('apps.productos.urls')),
    path('ordenes/', include('apps.ordenes.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    
 # Aquí incluimos las rutas API con prefijo 'api/'
    
    path('api/', include('apps.requerimientos.api_urls')),
 
    
    
    
    




    


]
