from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.requerimientos.models import Requerimiento
from apps.ordenes.models import OrdenCompra
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Crear grupos y asignar permisos según roles del proyecto"

    def handle(self, *args, **kwargs):
        # Crear grupos
        grupo_admin = Group.objects.get_or_create(name='Administrador')[0]
        grupo_almacen = Group.objects.get_or_create(name='Almacenero')[0]
        grupo_compras = Group.objects.get_or_create(name='Comprador')[0]
        grupo_solicitante = Group.objects.get_or_create(name='Solicitante')[0]

        # Permisos para Administrador: todos los permisos
        permisos_admin = Permission.objects.all()
        grupo_admin.permissions.set(permisos_admin)

        # Permisos para Almacenero: solo puede ver y cambiar productos y proveedores
        permisos_almacen = []
        # Permisos de Producto (ver y cambiar)
        ct_producto = ContentType.objects.get_for_model(Producto)
        permisos_almacen += Permission.objects.filter(content_type=ct_producto, codename__in=['view_producto', 'change_producto'])
        # Permisos de Proveedor (ver y cambiar)
        ct_proveedor = ContentType.objects.get_for_model(Proveedor)
        permisos_almacen += Permission.objects.filter(content_type=ct_proveedor, codename__in=['view_proveedor', 'change_proveedor'])
        grupo_almacen.permissions.set(permisos_almacen)

        # Permisos para Comprador: puede crear y ver requerimientos, crear y ver órdenes
        permisos_compras = []
        ct_requerimiento = ContentType.objects.get_for_model(Requerimiento)
        ct_orden = ContentType.objects.get_for_model(OrdenCompra)
        permisos_compras += Permission.objects.filter(content_type=ct_requerimiento, codename__in=['add_requerimiento', 'view_requerimiento'])
        permisos_compras += Permission.objects.filter(content_type=ct_orden, codename__in=['add_ordencompra', 'view_ordencompra'])
        grupo_compras.permissions.set(permisos_compras)

        # Permisos para Solicitante: solo puede crear y ver sus propios requerimientos
        permisos_solicitante = []
        permisos_solicitante += Permission.objects.filter(content_type=ct_requerimiento, codename__in=['add_requerimiento', 'view_requerimiento'])
        grupo_solicitante.permissions.set(permisos_solicitante)

        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados o actualizados correctamente'))
