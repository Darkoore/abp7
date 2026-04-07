##necesitamos formularios.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cuenta, Transaccion


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2', 'telefono', 'direccion']

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['numero_cuenta','tipo_cuenta']


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta_origen','cuenta_destino','tipo','monto','descripcion']