from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import UserExtension
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder': 'ej. Juan'}),
            'last_name':forms.TextInput(attrs={'placeholder': 'ej. Pérez Gómez'}),
            'username':forms.TextInput(attrs={'placeholder': 'ej. m-mendez96'}),
            'email':forms.TextInput(attrs={'placeholder': 'ej. mail-example@gmail.com'})
        }

class UserExtensionForm(forms.ModelForm):
    class Meta:
        model = UserExtension
        fields = ['identificacion','fecha_nacimiento','telefono','direccion']
        widgets = {
            'identificacion':forms.TextInput(attrs={'placeholder': 'ej. V-19348289'}),
            'fecha_nacimiento':forms.TextInput(attrs={'placeholder': 'ej. 21/05/1994'}),
            'telefono':forms.TextInput(attrs={'placeholder': 'ej. +58 412 1002038'}),
            'direccion':forms.TextInput(attrs={'placeholder': 'ej. Av. Las Americas, Residencias El Parque, ...'})
        }
