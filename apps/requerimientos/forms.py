from django import forms
from .models import DetalleRequerimiento
from .models import Requerimiento


class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['nombre', 'solicitante', 'departamento', 'prioridad', 'estado']
        

class DetalleRequerimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleRequerimiento
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RequerimientoSolicitanteForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = ['nombre', 'departamento', 'prioridad']
        widgets = {
            'departamento': forms.HiddenInput(),  # Ocultamos porque será asignado automático
        }

        