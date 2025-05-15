from django.shortcuts import render, get_object_or_404, redirect
from .models import Requerimiento, DetalleRequerimiento
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from apps.productos.models import Producto
from .forms import DetalleRequerimientoForm
from django.contrib.auth.decorators import login_required, permission_required

# --- Lista de Requerimientos ---
@login_required
@permission_required('requerimientos.view_requerimiento', raise_exception=True)
def lista_requerimientos(request):
    requerimientos = Requerimiento.objects.all().order_by('-fecha')
    return render(request, 'requerimientos/lista.html', {'requerimientos': requerimientos})

# --- Crear Requerimiento ---
@login_required
@permission_required('requerimientos.add_requerimiento', raise_exception=True)
def crear_requerimiento(request):
    if request.method == 'POST':
        solicitante_id = request.POST.get('solicitante')
        departamento_id = request.POST.get('departamento')
        prioridad = request.POST.get('prioridad')
        
        solicitante = Usuario.objects.get(id=solicitante_id)
        departamento = Departamento.objects.get(id=departamento_id)

        requerimiento = Requerimiento.objects.create(
            solicitante=solicitante,
            departamento=departamento,
            prioridad=prioridad,
            estado='pendiente'
        )
        return redirect('lista_requerimientos')  # Redirige a la lista de requerimientos

    usuarios = Usuario.objects.all()
    departamentos = Departamento.objects.all()
    prioridades = Requerimiento.PRIORIDAD_CHOICES
    return render(request, 'requerimientos/formulario.html', {
        'usuarios': usuarios,
        'departamentos': departamentos,
        'prioridades': prioridades
    })

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
            return redirect('agregar_detalle_requerimiento', requerimiento_id=requerimiento.id)
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
        requerimiento.delete()
        return redirect('lista_requerimientos')  # Redirige a la lista de requerimientos
    return render(request, 'requerimientos/confirmar_eliminacion.html', {'requerimiento': requerimiento})

# --- Editar Requerimiento ---
@login_required
@permission_required('requerimientos.change_requerimiento', raise_exception=True)
def editar_requerimiento(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, pk=requerimiento_id)
    if request.method == 'POST':
        form = DetalleRequerimientoForm(request.POST, instance=requerimiento)
        if form.is_valid():
            form.save()
            return redirect('lista_requerimientos')  # Redirige a la lista de requerimientos
    else:
        form = DetalleRequerimientoForm(instance=requerimiento)

    return render(request, 'requerimientos/formulario.html', {'form': form})
