from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models.models import *
from django.contrib.auth.models import *








class CreacionUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {'username': 'Nombre de Usuario', 'password1': 'Contraseña', 'password2': 'Comprobar Contraseña'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'minlength':'8', 'maxlength':'30'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Comprobar Contraseña', 'minlength':'8', 'maxlength':'30'}),
        }












class CrearTrabajadorForm(forms.ModelForm):
    
    class Meta:
        model = Trabajador    
        fields = '__all__'
        labels = {'usuario': ''}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos':forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'horas_ocupadas': forms.NumberInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'institucion': forms.Select(attrs={'class': 'form-control'}),
            'especializacion': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'invisible'}),
        }
    














class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {'username': 'Nombre de Usuario'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
        }













class EditarTrabajadorForm(forms.ModelForm):
    
    class Meta:
        model = Trabajador    
        fields = {'nombre','apellidos','sexo','departamento','institucion'}
        widgets = {
            
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos':forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'institucion': forms.Select(attrs={'class': 'form-control'}),
        }
    


        