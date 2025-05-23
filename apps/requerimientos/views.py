from django.shortcuts import render, get_object_or_404, redirect
from .models import Requerimiento, DetalleRequerimiento, HistorialAprobacion
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from .forms import DetalleRequerimientoForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RequerimientoSolicitanteForm
from .forms import RequerimientoForm
from apps.productos.models import Categoria, Producto
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group






# --- Lista de Requerimientos ---
@login_required
@permission_required('requerimientos.view_requerimiento', raise_exception=True)
def lista_requerimientos(request):
    requerimientos = Requerimiento.objects.filter(activo=True).order_by('-fecha')
    return render(request, 'requerimientos/lista.html', {'requerimientos': requerimientos})


# --- Crear Requerimiento ---
@login_required
@permission_required('requerimientos.add_requerimiento', raise_exception=True)
def crear_requerimiento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        prioridad = request.POST.get('prioridad')
        solicitante_id = request.POST.get('solicitante')
        departamento_id = request.POST.get('departamento')

        solicitante = get_object_or_404(Usuario, pk=solicitante_id)
        departamento = get_object_or_404(Departamento, pk=departamento_id)

        requerimiento = Requerimiento.objects.create(
            nombre=nombre,
            solicitante=solicitante,
            departamento=departamento,
            prioridad=prioridad,
            estado='pendiente'
        )

        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        for prod_id, cant in zip(productos_ids, cantidades):
            producto = Producto.objects.get(id=prod_id)
            DetalleRequerimiento.objects.create(
                requerimiento=requerimiento,
                producto=producto,
                cantidad=int(cant)
            )

        return redirect('lista_requerimientos')

    usuarios = Usuario.objects.filter(groups__name='solicitante', is_active=True)
    print("Usuarios disponibles:", usuarios)
    departamentos = Departamento.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    prioridades = Requerimiento.PRIORIDAD_CHOICES

    print("Usuarios cargados como solicitantes:", usuarios)
    return render(request, 'requerimientos/formulario.html', {
        'requerimiento': None,  # Indica que es nuevo
        'usuarios': usuarios,
        'departamentos': departamentos,
        'categorias': categorias,
        'prioridades': prioridades
    })

    
    #requerimiento creado desde admin
    from django import forms
from .models import Requerimiento, Usuario, Departamento

class RequerimientoAdminForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['nombre', 'prioridad', 'solicitante', 'departamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solicitante'].queryset = Usuario.objects.filter(rol__nombre='Solicitante', is_active=True)
        self.fields['departamento'].queryset = Departamento.objects.filter(activo=True)


# --- Agregar Detalle al Requerimiento ---
@login_required
@permission_required('requerimientos.add_detalle', raise_exception=True)
def agregar_detalle_requerimiento(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = DetalleRequerimientoForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.requerimiento = requerimiento
            detalle.save()
            return redirect('lista_requerimientos_solicitante')
    else:
        form = DetalleRequerimientoForm()

    detalles_existentes = requerimiento.detalles.all()

    # Pasar la información del requerimiento para mostrar solicitante, departamento y prioridad
    return render(request, 'requerimientos/agregar_detalle.html', {
        'form': form,
        'requerimiento': requerimiento,
        'detalles_existentes': detalles_existentes,
        'productos': productos
    })


# --- Eliminar Requerimiento ---
@login_required
@permission_required('requerimientos.delete_requerimiento', raise_exception=True)
def eliminar_requerimiento(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    if request.method == 'POST':
        requerimiento.activo = False
        requerimiento.save()
        return redirect('lista_requerimientos_solicitante')  # O redirigir según rol
    return render(request, 'requerimientos/confirmar_eliminacion.html', {'requerimiento': requerimiento})

# --- Editar Requerimiento ---
@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def editar_requerimiento(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)

    if request.method == 'POST':
        requerimiento.nombre = request.POST.get('nombre')
        requerimiento.prioridad = request.POST.get('prioridad')
        solicitante_id = request.POST.get('solicitante')
        departamento_id = request.POST.get('departamento')

        requerimiento.solicitante = get_object_or_404(Usuario, pk=solicitante_id)
        requerimiento.departamento = get_object_or_404(Departamento, pk=departamento_id)
        requerimiento.save()

        requerimiento.detalles.all().delete()

        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        for prod_id, cant in zip(productos_ids, cantidades):
            producto = Producto.objects.get(id=prod_id)
            DetalleRequerimiento.objects.create(
                requerimiento=requerimiento,
                producto=producto,
                cantidad=int(cant)
            )

        messages.success(request, "Requerimiento actualizado correctamente.")
        return redirect('lista_requerimientos')

    usuarios = Usuario.objects.filter(groups__name='solicitante', is_active=True)
    departamentos = Departamento.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    prioridades = Requerimiento.PRIORIDAD_CHOICES

    return render(request, 'requerimientos/formulario.html', {
        'requerimiento': requerimiento,
        'usuarios': usuarios,
        'departamentos': departamentos,
        'categorias': categorias,
        'prioridades': prioridades
    })


#solicitante
@login_required
def lista_requerimientos_solicitante(request):
    usuario = request.user
    requerimientos = Requerimiento.objects.filter(solicitante=usuario, activo=True).order_by('-fecha')
    return render(request, 'requerimientos/mis_requerimientos.html', {'requerimientos': requerimientos})

# API para obtener productos por categoría
def productos_por_categoria(request, categoria_id):
    productos = Producto.objects.filter(categoria_id=categoria_id, activo=True)
    data = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse(data, safe=False)


@login_required
def crear_requerimiento_solicitante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        prioridad = request.POST.get('prioridad')
        solicitante = request.user

        if not solicitante.departamento:
            # manejar el error o redirigir con mensaje
            messages.error(request, "No tiene un departamento asignado. Contacte con el administrador.")
            return redirect('lista_requerimientos_solicitante')

        departamento = solicitante.departamento

        requerimiento = Requerimiento.objects.create(
            nombre=nombre,
            prioridad=prioridad,
            solicitante=solicitante,
            departamento=departamento,
            estado='pendiente',
            activo=True
        )

        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        for prod_id, cant in zip(productos_ids, cantidades):
            producto = Producto.objects.get(pk=prod_id)
            DetalleRequerimiento.objects.create(
                requerimiento=requerimiento,
                producto=producto,
                cantidad=int(cant)
            )

        return redirect('lista_requerimientos_solicitante')

    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'requerimientos/formulario_solicitante.html', {
    'categorias': categorias,
    'detalle_productos': [],  # <- NECESARIO para evitar errores con JSON.parse
    'modo': 'crear'           # <- NECESARIO para mostrar correctamente el título, etc.
    })

@login_required
def editar_requerimiento_solicitante(request, requerimiento_id):
    # Obtener el requerimiento y verificar que pertenece al usuario actual
    requerimiento = get_object_or_404(Requerimiento, id=requerimiento_id, solicitante=request.user)
    
    # Verificar que el requerimiento se puede editar (solo pendientes o rechazados)
    if requerimiento.estado not in ['pendiente', 'rechazado']:
        messages.error(request, "No puede editar un requerimiento que ya ha sido procesado.")
        return redirect('lista_requerimientos_solicitante')

    if request.method == 'POST':
        # Guardar cambios al requerimiento
        requerimiento.nombre = request.POST.get('nombre')
        requerimiento.prioridad = request.POST.get('prioridad')
        requerimiento.save()

        # Limpiar detalles antiguos y guardar nuevos
        requerimiento.detalles.all().delete()

        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        for prod_id, cant in zip(productos_ids, cantidades):
            producto = Producto.objects.get(pk=prod_id)
            DetalleRequerimiento.objects.create(
                requerimiento=requerimiento,
                producto=producto,
                cantidad=int(cant)
            )
        messages.success(request, "Requerimiento actualizado correctamente.")
        return redirect('lista_requerimientos_solicitante')

    else:
        # Preparar detalles para pre-cargar en el JS del template
        detalle_productos = []
        for detalle in requerimiento.detalles.all():
            detalle_productos.append({
                'id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'cantidad': detalle.cantidad,
                'categoria_id': detalle.producto.categoria.id
            })

        categorias = Categoria.objects.filter(activo=True)
        prioridades = Requerimiento.PRIORIDAD_CHOICES
        usuarios = Usuario.objects.filter(groups__name='solicitante', is_active=True)
        departamentos = Departamento.objects.filter(activo=True)

        context = {
            'categorias': categorias,
            'prioridades': prioridades,
            'form': requerimiento,
            'detalle_productos': detalle_productos,
            'modo': 'editar',
            'usuarios': usuarios,
            'departamentos': departamentos,
        }
        return render(request, 'requerimientos/formulario_solicitante.html', context)



@login_required
def eliminar_requerimiento_solicitante(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, solicitante=request.user)
    
    # Verificar que el requerimiento se puede eliminar (solo pendientes)
    if requerimiento.estado != 'pendiente':
        messages.error(request, "Solo puede eliminar requerimientos pendientes.")
        return redirect('lista_requerimientos_solicitante')
        
    if request.method == 'POST':
        requerimiento.activo = False
        requerimiento.save()
        messages.success(request, "Requerimiento eliminado correctamente.")
        return redirect('lista_requerimientos_solicitante')
    return render(request, 'requerimientos/confirmar_eliminacion.html', {'requerimiento': requerimiento})


# ====== VISTAS PARA APROBADOR ======

@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def lista_requerimientos_aprobador(request):
    """Vista para mostrar lista de requerimientos pendientes de aprobación"""
    requerimientos = Requerimiento.objects.filter(
        activo=True,
        estado='pendiente'
    ).order_by('-fecha')
    
    return render(request, 'requerimientos/lista_aprobador.html', {
        'requerimientos': requerimientos
    })


@login_required
@permission_required('requerimientos.view_requerimiento', raise_exception=True)
def ver_detalle_requerimiento(request, requerimiento_id):
    """Vista para ver el detalle completo de un requerimiento"""
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, activo=True)
    
    # Obtener los detalles (productos) del requerimiento
    detalles = DetalleRequerimiento.objects.filter(requerimiento=requerimiento)
    
    # Obtener el historial de aprobaciones si existe
    historial = []
    if hasattr(requerimiento, 'historialaprobacion_set'):
        historial = requerimiento.historialaprobacion_set.all().order_by('-fecha')
    
    return render(request, 'requerimientos/detalle_requerimiento.html', {
        'requerimiento': requerimiento,
        'detalles': detalles,
        'historial': historial
    })


@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def aprobar_requerimiento(request, requerimiento_id):
    """Vista para aprobar un requerimiento"""
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, activo=True)
    
    # Verificar que el requerimiento esté pendiente
    if requerimiento.estado != 'pendiente':
        messages.error(request, "Este requerimiento ya ha sido procesado.")
        return redirect('ver_detalle_requerimiento', requerimiento_id=requerimiento.id)
    
    if request.method == 'POST':
        observacion = request.POST.get('observacion', '')
        
        # Cambiar el estado del requerimiento
        requerimiento.estado = 'aprobado'
        requerimiento.save()
        
        # Crear registro en el historial si tienes ese modelo
        try:
            HistorialAprobacion.objects.create(
                requerimiento=requerimiento,
                usuario=request.user,
                accion='aprobado',
                observacion=observacion,
                fecha=timezone.now()
            )
        except:
            # Si no tienes el modelo HistorialAprobacion, omite esta parte
            pass
        
        messages.success(request, f"Requerimiento #{requerimiento.id} aprobado correctamente.")
        return redirect('lista_requerimientos_aprobador')
    
    return render(request, 'requerimientos/confirmar_aprobacion.html', {
        'requerimiento': requerimiento,
        'accion': 'aprobar'
    })


@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def rechazar_requerimiento(request, requerimiento_id):
    """Vista para rechazar un requerimiento"""
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id, activo=True)
    
    # Verificar que el requerimiento esté pendiente
    if requerimiento.estado != 'pendiente':
        messages.error(request, "Este requerimiento ya ha sido procesado.")
        return redirect('ver_detalle_requerimiento', requerimiento_id=requerimiento.id)
    
    if request.method == 'POST':
        observacion = request.POST.get('observacion', '')
        
        # Cambiar el estado del requerimiento
        requerimiento.estado = 'rechazado'
        requerimiento.save()
        
        # Crear registro en el historial si tienes ese modelo
        try:
            HistorialAprobacion.objects.create(
                requerimiento=requerimiento,
                usuario=request.user,
                accion='rechazado',
                observacion=observacion,
                fecha=timezone.now()
            )
        except:
            # Si no tienes el modelo HistorialAprobacion, omite esta parte
            pass
        
        messages.success(request, f"Requerimiento #{requerimiento.id} rechazado correctamente.")
        return redirect('lista_requerimientos_aprobador')
    
    return render(request, 'requerimientos/confirmar_aprobacion.html', {
        'requerimiento': requerimiento,
        'accion': 'rechazar'
    })