from django.shortcuts import render, get_object_or_404, redirect
from .models import Departamento
from .forms import DepartamentoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

@login_required
@permission_required('departamentos.view_departamento', raise_exception=True)
def lista_departamentos(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentos/lista.html', {'departamentos': departamentos})

@login_required
@permission_required('departamentos.add_departamento', raise_exception=True)
def crear_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            departamento = form.save()
            messages.success(request, f'Departamento "{departamento.nombre}" creado exitosamente.')
            return redirect('lista_departamentos')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = DepartamentoForm()
    return render(request, 'departamentos/formulario.html', {'form': form})

@login_required
@permission_required('departamentos.change_departamento', raise_exception=True)
def editar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, pk=departamento_id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            departamento = form.save()
            messages.success(request, f'Departamento "{departamento.nombre}" actualizado exitosamente.')
            return redirect('lista_departamentos')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentos/formulario.html', {'form': form})

@login_required
@permission_required('departamentos.delete_departamento', raise_exception=True)
def eliminar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, pk=departamento_id)
    if request.method == 'POST':
        nombre_departamento = departamento.nombre
        departamento.delete()
        messages.success(request, f'Departamento "{nombre_departamento}" eliminado exitosamente.')
        return redirect('lista_departamentos')
    return render(request, 'departamentos/confirmar_eliminacion.html', {'departamento': departamento})

@login_required
@permission_required('departamentos.change_departamento', raise_exception=True)
def toggle_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, pk=departamento_id)
    
    # Cambiar el estado del departamento
    departamento.activo = not departamento.activo
    departamento.save()
    
    # Mensaje de confirmación
    estado = "activado" if departamento.activo else "desactivado"
    messages.success(request, f'Departamento "{departamento.nombre}" {estado} exitosamente.')
    
    return redirect('lista_departamentos')