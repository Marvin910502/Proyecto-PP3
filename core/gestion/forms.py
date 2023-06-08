from django import forms
from core.models.models import *
from django.contrib.auth.models import *
from django.db.models import Q


class DateInput(forms.DateInput):
    input_type = 'date-local'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date-local'


class CreacionInvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['nombre', 'descripcion', 'horas_mensuales_necesarias', 'trabajador']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'horas_mensuales_necesarias': forms.NumberInput(attrs={'class': 'form-control'}),
            'trabajador': forms.CheckboxSelectMultiple(),

        }  

    def __init__(self, *args, trabajador, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.filter(horas_ocupadas__lt=160).exclude(id=trabajador.id).order_by('nombre')


class EdicionInvestigacionForm(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = ['nombre', 'descripcion', 'horas_mensuales_necesarias', 'trabajador']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'horas_mensuales_necesarias': forms.NumberInput(attrs={'class': 'form-control'}),
            'trabajador': forms.CheckboxSelectMultiple(),

        }

    def __init__(self, *args, trabajador, investigacion,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.exclude(Q(horas_ocupadas__gte=160) & ~Q(investigacion=investigacion)).order_by('nombre')


class CreacionTareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        exclude = ['evento', 'publicacion', 'informe_sem', 'informe_final', 'investigacion', 'fecha_culminacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'horas_necesarias': forms.NumberInput(attrs={'class': 'form-control'}),
            'trabajador': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, investigacion, **kwargs,):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.filter(investigacion=investigacion).order_by('nombre')


class ParteForm(forms.ModelForm):
    class Meta:
        model = Parte_Hora  
        fields = '__all__'
        labels = {'tarea': '', 'trabajador': '', 'fecha': '', 'horas_dedicadas': '', 'descripcion': ''}
        widgets = {
            'tarea': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tarea'}),
            'trabajador': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Trabajador'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha', 'type': 'date'}),
            'horas_dedicadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': '1'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajador'].queryset = Trabajador.objects.all()
        self.fields['tarea'].queryset = Tarea.objects.all()












