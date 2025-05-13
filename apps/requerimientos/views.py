from django.shortcuts import render, get_object_or_404
from .models import Requerimiento
from django.http import HttpResponse

def lista_requerimientos(request):
    requerimientos = Requerimiento.objects.all().order_by('-fecha')
    return render(request, 'requerimientos/lista.html', {'requerimientos': requerimientos})


# Create your views here.
