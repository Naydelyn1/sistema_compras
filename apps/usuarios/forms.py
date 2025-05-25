from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re
from apps.departamentos.models import Departamento


Usuario = get_user_model()

class UsuarioCreacionForm(UserCreationForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(), 
        required=False,
        empty_label="Seleccione un departamento"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'is_active', 'groups', 'departamento']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden. Por favor, verifica.")

        if password1 and password1.isdigit():
            raise ValidationError("La contraseña no puede ser solo numérica. Incluye letras o símbolos.")

        if password1 and len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if password1 and not re.search(r'[A-Z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")

        if password1 and not re.search(r'[a-z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")

        if password1 and not re.search(r'[\W_]', password1):
            raise ValidationError("La contraseña debe contener al menos un símbolo o carácter especial.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
       
        user.first_name = self.cleaned_data.get('nombre', '')
        user.last_name = self.cleaned_data.get('apellido', '')
        
        if commit:
            user.save()
            self.save_m2m()  
        return user


class UsuarioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False,
        empty_label="Seleccione un departamento"
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'departamento']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['departamento'].required = False
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['groups'].widget.attrs.update({'class': 'form-select'})
        self.fields['departamento'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = user.first_name
        user.apellido = user.last_name
        
        if commit:
            user.save()
            self.save_m2m()  
        return user


# Formulario adicional para cambio de contraseña si lo necesitas
class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña actual"
    )
    password_nueva = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Nueva contraseña"
    )
    password_confirmacion = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar nueva contraseña"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password_nueva = cleaned_data.get('password_nueva')
        password_confirmacion = cleaned_data.get('password_confirmacion')
        
        if password_nueva and password_confirmacion:
            if password_nueva != password_confirmacion:
                raise ValidationError("Las contraseñas nuevas no coinciden.")
        
        return cleaned_data