from django import forms
from core.models.models import *
from django.contrib.auth.models import *


class DateInput(forms.DateInput):
    input_type = 'date-local'






class DateTimeInput(forms.DateTimeInput):
    input_type = 'date-local'







class CreacionInvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['nombre', 'descripcion', 'completado','trabajador'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'completado': forms.NumberInput(attrs={'class': 'form-control'}),
            'trabajador': forms.CheckboxSelectMultiple(),

        }  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.all()









class CreacionTareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        exclude = ['evento', 'publicacion', 'informe_sem', 'informe_final','investigacion','fecha_culminacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'horas_necesarias': forms.NumberInput(attrs={'class': 'form-control'}),
            'trabajador': forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.all()









class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte_Hora  
        fields = '__all__'
        labels = {'tarea': '', 'trabajador': '', 'fecha': '', 'horas_dedicadas': '', 'descripcion': ''}
        widgets = {
            'tarea': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tarea'}),
            'trabajador': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Trabajador'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha', 'type': 'date', 'default': '2023-02-05'}),
            'horas_dedicadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': '1'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.all()
        self.fields['tarea'].queryset = Tarea.objects.all()












