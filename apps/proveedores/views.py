from django.shortcuts import render, redirect
from .models import Proveedor
from .forms import ProveedorForm

def lista_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('-fecha_registro')
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/formulario.html', {'form': form})



# Create your views here.
