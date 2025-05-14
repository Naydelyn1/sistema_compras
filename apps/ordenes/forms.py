from django import forms
from .models import OrdenCompra, DetalleOrdenCompra

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['codigo', 'requerimiento', 'proveedor', 'usuario_emisor', 'fecha_entrega_estimada', 'estado', 'condiciones_pago']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'requerimiento': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'usuario_emisor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }
