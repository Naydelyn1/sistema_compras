from django.urls import path
from . import views

urlpatterns = [
    # URL para lista de órdenes (FALTABA ESTA)
    path('lista/', views.lista_ordenes, name='lista_ordenes'),
    
    # URLs existentes
    path('', views.lista_requerimientos_aprobados, name='lista_requerimientos_aprobados'),
    path('requerimiento/<int:requerimiento_id>/detalle/', views.ver_detalle_requerimiento_comprador, name='ver_detalle_requerimiento_comprador'),
    path('requerimiento/<int:requerimiento_id>/asignar-proveedores/', views.asignar_proveedores, name='asignar_proveedores'),
    path('requerimiento/<int:requerimiento_id>/generar-orden/', views.generar_orden_compra, name='generar_orden_compra'),
    path('requerimiento/<int:requerimiento_id>/resumen-ordenes/', views.resumen_ordenes_generadas, name='resumen_ordenes_generadas'),
    path('mis-ordenes/', views.mis_ordenes_generadas, name='mis_ordenes_generadas'),
    path('ajax/aplicar-proveedor-categoria/', views.aplicar_proveedor_categoria, name='aplicar_proveedor_categoria'),
]