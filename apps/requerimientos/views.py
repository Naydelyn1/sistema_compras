from django.shortcuts import render, get_object_or_404, redirect
from .models import Requerimiento, DetalleRequerimiento
from apps.usuarios.models import Usuario
from apps.departamentos.models import Departamento
from apps.productos.models import Producto
from .forms import DetalleRequerimientoForm


def lista_requerimientos(request):
    requerimientos = Requerimiento.objects.all().order_by('-fecha')
    return render(request, 'requerimientos/lista.html', {'requerimientos': requerimientos})


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
        return redirect('lista_requerimientos')

    usuarios = Usuario.objects.all()
    departamentos = Departamento.objects.all()
    prioridades = Requerimiento.PRIORIDAD_CHOICES
    return render(request, 'requerimientos/formulario.html', {
        'usuarios': usuarios,
        'departamentos': departamentos,
        'prioridades': prioridades
    })


def agregar_detalle_requerimiento(request, requerimiento_id):
    requerimiento = get_object_or_404(Requerimiento, id=requerimiento_id)

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
    return render(request, 'requerimientos/agregar_detalle.html', {
        'form': form,
        'requerimiento': requerimiento,
        'detalles_existentes': detalles_existentes
    })