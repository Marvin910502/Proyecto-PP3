from django.shortcuts import render, redirect, HttpResponseRedirect
from core.models.models import *
from django.contrib.auth.decorators import *
from .forms import *


# Create your views here.


@login_required()
def Menu_Investigaciones(request):
    Proyectos = Investigacion.objects.order_by('nombre')
    trabajador = Trabajador.objects.all() 
    title = 'Gestor CFA'
    section = 'Investigaciones'

    context = {
        'Proyectos': Proyectos,
        'title': title,
        'section': section,
        'trabajador': trabajador,
    }
    return render(request, 'website/menu_investigaciones.html', context)


@login_required()
def Tarea_View(request, investigacion_nombre):
    Tareas = Tarea.objects.order_by('nombre')
    Investigaciones = Investigacion.objects.all()
    for investigacion in Investigaciones:        
        if investigacion.nombre == investigacion_nombre:
            descripcion = investigacion.descripcion
            participantes = investigacion.trabajador.all()

    context = {
        'Tareas': Tareas,
        'title': 'Gestor CFA',
        'section': 'Tareas',
        'investigacion_nombre': investigacion_nombre,
        'descripcion': descripcion,
        'participantes': participantes,
    }
    return render(request, 'website/menu_tareas.html', context)


@login_required()
def Tarea_Contenido(request, tarea_nombre, nombre_usuario):
    tarea_actual = Tarea.objects.filter(nombre=tarea_nombre).first()
    participantes = tarea_actual.trabajador.all()
    parte_de_horas = Parte_Hora.objects.filter(tarea = tarea_actual).order_by('fecha')
    user = User.objects.filter(username = nombre_usuario).first()
    trab = Trabajador.objects.filter(usuario = user).first()
    edicion = False
    if request.method == 'POST':
        parte_hora_form = ParteForm(request.POST)
        if parte_hora_form.is_valid():
            parte = parte_hora_form.save(commit=False)
            parte.tarea = tarea_actual
            parte.trabajador = trab
            parte.save()
            return redirect('tarea_contenido', tarea_nombre, nombre_usuario)
    else:
        parte_hora_form = ParteForm()
    return render(request, 'website/tarea.html', {'tarea_actual':tarea_actual, 'participantes': participantes, 'parte_de_horas': parte_de_horas, 'parte_horas_form': parte_hora_form, 'edicion': edicion, 'trab': trab})


@login_required()
def Editar_Parte(request, tarea_nombre, id_parte):

    tarea_actual = Tarea.objects.filter(nombre=tarea_nombre).first()
    participantes = tarea_actual.trabajador.all()
    parte = Parte_Hora.objects.get(id = id_parte)
    parte_de_horas = Parte_Hora.objects.filter(tarea = tarea_actual).order_by('fecha')
    nombre_usuario = parte.trabajador.usuario
    edicion = True
    if request.method == 'POST':
        parte_hora_form = ParteForm(request.POST, instance = parte)
        if parte_hora_form.is_valid():
            part = parte_hora_form.save(commit=False)
            part.tarea = tarea_actual
            part.fecha = parte.fecha
            part.save()
            return redirect('tarea_contenido', tarea_nombre, nombre_usuario)
    else:
        parte_hora_form = ParteForm(instance = parte)
    return render(request, 'website/tarea.html', {'tarea_actual':tarea_actual, 'participantes': participantes, 'parte_de_horas': parte_de_horas, 'parte_horas_form': parte_hora_form, 'edicion': edicion, 'id_parte': id_parte})


@login_required()
def Eliminar_Parte(request, id_parte, tarea_nombre):
    parte = Parte_Hora.objects.get(id = id_parte)
    nombre_usuario = parte.trabajador.usuario
    parte.delete()
    return redirect('tarea_contenido', tarea_nombre, nombre_usuario)


@login_required()
def Crear_Investigacion(request):
    if request.method == 'POST':
        Investigacion_From = CreacionInvestigacionForm(request.POST)
        if Investigacion_From.is_valid():
            Investigacion_From.save()
            return redirect('home')
    else:
        Investigacion_From = CreacionInvestigacionForm()
    return render(request, 'website/crear_investigacion.html', {'Investigacion_Form': Investigacion_From})


@login_required()
def Editar_Investigacion(request, id_investigacion):
    investigacion = Investigacion.objects.get(id = id_investigacion)
    if request.method == 'POST':
        Edit_Investigacion_From = CreacionInvestigacionForm(request.POST, instance=investigacion)       
        if Edit_Investigacion_From.is_valid():
            Edit_Investigacion_From.save()
            return redirect('home')
    else:
        Edit_Investigacion_From = CreacionInvestigacionForm(instance=investigacion)
    return render(request, 'website/editar_investigacion.html', {'Edit_Investigacion_Form': Edit_Investigacion_From})


@login_required()
def Crear_Tarea(request, investigacion_nombre):
    investigacion = Investigacion.objects.filter(nombre=investigacion_nombre).first()
    if request.method == 'POST':
        Tarea_From = CreacionTareaForm(request.POST)
        if Tarea_From.is_valid():
            tarea = Tarea_From.save()
            tarea.investigacion = investigacion
            tarea.save()
            return redirect('tarea_view', investigacion_nombre)
    else:
        Tarea_From = CreacionTareaForm()
    return render(request, 'website/crear_tarea.html', {'Tarea_Form': Tarea_From})


@login_required()
def Editar_Tarea(request, id_tarea):
    tarea = Tarea.objects.get(id = id_tarea)
    if request.method == 'POST':
        Edit_Tarea_From = CreacionTareaForm(request.POST, instance=tarea)       
        if Edit_Tarea_From.is_valid():
            Edit_Tarea_From.save()
            return redirect('tarea_view', tarea.investigacion)
    else:
        Edit_Tarea_From = CreacionTareaForm(instance=tarea)
    return render(request, 'website/editar_tarea.html', {'Edit_Tarea_Form': Edit_Tarea_From})

















