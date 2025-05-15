from django.shortcuts import render, get_object_or_404, redirect
from .models import Departamento
from .forms import DepartamentoForm

def lista_departamentos(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentos/lista.html', {'departamentos': departamentos})

def crear_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_departamentos')
    else:
        form = DepartamentoForm()
    return render(request, 'departamentos/formulario.html', {'form': form})

def editar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, pk=departamento_id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('lista_departamentos')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentos/formulario.html', {'form': form})

def eliminar_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, pk=departamento_id)
    if request.method == 'POST':
        departamento.delete()
        return redirect('lista_departamentos')
    return render(request, 'departamentos/confirmar_eliminacion.html', {'departamento': departamento})



# Create your views here.
