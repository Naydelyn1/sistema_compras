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
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'is_active', 'groups']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden. Por favor, verifica.")

        if password1.isdigit():
            raise ValidationError("La contraseña no puede ser solo numérica. Incluye letras o símbolos.")

        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[A-Z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")

        if not re.search(r'[a-z]', password1):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula.")

        if not re.search(r'[\W_]', password1):
            raise ValidationError("La contraseña debe contener al menos un símbolo o carácter especial.")

        return password2


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'is_active',  'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departamento'].required = False

        
   