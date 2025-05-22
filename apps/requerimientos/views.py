from django.shortcuts import render, get_object_or_404, redirect
from .models import Requerimiento, DetalleRequerimiento
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from .forms import DetalleRequerimientoForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RequerimientoSolicitanteForm
from .forms import RequerimientoForm
from apps.productos.models import Categoria, Producto
from django.http import JsonResponse
from django.contrib import messages



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

        # Solicitante y departamento se asignan desde usuario logueado
        solicitante = request.user
        departamento = solicitante.departamento

        # Crear el requerimiento
        requerimiento = Requerimiento.objects.create(
            nombre=nombre,
            solicitante=solicitante,
            departamento=departamento,
            prioridad=prioridad,
            estado='pendiente'
        )

        # Procesar productos y cantidades
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')

        for prod_id, cant in zip(productos_ids, cantidades):
            producto = Producto.objects.get(id=prod_id)
            DetalleRequerimiento.objects.create(
                requerimiento=requerimiento,
                producto=producto,
                cantidad=int(cant)
            )

        return redirect('lista_requerimientos_solicitante')  # O la url que uses para lista solicitante

    categorias = Categoria.objects.all()
    prioridades = Requerimiento.PRIORIDAD_CHOICES

    return render(request, 'requerimientos/formulario_solicitante.html', {
        'categorias': categorias,
        'prioridades': prioridades,
        # No enviamos solicitantes ni departamentos para elegir,
        # ya que se asignan automáticamente
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
        requerimiento.activo = False
        requerimiento.save()
        return redirect('lista_requerimientos')  # O redirigir según rol
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
    return render(request, 'requerimientos/formulario_solicitante.html', {'categorias': categorias})

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
                'cantidad': detalle.cantidad
            })

        categorias = Categoria.objects.filter(activo=True)
        prioridades = Requerimiento.PRIORIDAD_CHOICES

        context = {
            'categorias': categorias,
            'prioridades': prioridades,
            'form': requerimiento,
            'detalle_productos': detalle_productos,
            'modo': 'editar',
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