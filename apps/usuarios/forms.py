from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class UsuarioCreacionForm(UserCreationForm):
    cargo = forms.CharField(required=False, label="Cargo")
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Roles"
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'apellido', 'cargo', 'groups')


class UsuarioForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Roles"
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'cargo', 'is_active', 'groups']
        
   