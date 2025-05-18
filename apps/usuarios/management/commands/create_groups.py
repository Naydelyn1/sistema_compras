from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import Usuario  # Ejemplo, cambia según necesidad

class Command(BaseCommand):
    help = 'Crea grupos y asigna permisos básicos para roles del sistema'

    def handle(self, *args, **kwargs):
        # Define roles y permisos básicos para cada uno
        roles_permisos = {
        'administrador': {
            'apps': ['usuarios', 'departamentos', 'proveedores', 'productos', 'requerimientos', 'ordenes'],
            'permisos': ['add', 'change', 'delete', 'view'],
        },
        'solicitante': {
            'apps': ['requerimientos'],
            'permisos': ['add', 'view'],
        },
        'aprobador': {
            'apps': ['requerimientos'],
            'permisos': ['change', 'view'],
        },
        'comprador': {
            'apps': ['ordenes'],
            'permisos': ['add', 'change', 'view'],
        },
        'usuario_estandar': {
            'apps': ['usuarios', 'departamentos', 'proveedores', 'productos', 'requerimientos', 'ordenes'],
            'permisos': ['view'],
        },
    }
        


        for rol, config in roles_permisos.items():
            group, created = Group.objects.get_or_create(name=rol)
            self.stdout.write(f"{'Creando' if created else 'Actualizando'} grupo: {rol}")

            # Limpia permisos actuales para evitar duplicados
            group.permissions.clear()

            for app_label in config['apps']:
                content_types = ContentType.objects.filter(app_label=app_label)
                for ct in content_types:
                    for codename_prefix in config['permisos']:
                        codename = f"{codename_prefix}_{ct.model}"
                        try:
                            permiso = Permission.objects.get(codename=codename)
                            group.permissions.add(permiso)
                            self.stdout.write(f"  Agregado permiso {codename} para app {app_label}")
                        except Permission.DoesNotExist:
                            self.stdout.write(f"  No existe permiso {codename} para app {app_label}")

            group.save()

        self.stdout.write("Grupos y permisos creados/actualizados correctamente.")
