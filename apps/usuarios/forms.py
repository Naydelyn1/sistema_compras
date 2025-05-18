from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        # Aquí defines los campos que quieres que se puedan llenar al crear usuario
        fields = ('username', 'nombre', 'apellido', 'email', 'password1', 'password2', 'cargo')


class UsuarioForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Roles"
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'is_active', 'groups']
        
   