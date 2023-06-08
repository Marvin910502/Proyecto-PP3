from django.shortcuts import render, redirect, HttpResponseRedirect
from core.models.models import *
from django.contrib.auth.decorators import *
from .forms import *


# Create your views here.



@login_required()
def Menu_Investigaciones(request):
    usuario_login = request.user
    trabajador_login = Trabajador.objects.filter(id=usuario_login.id).first()
    Proyectos = Investigacion.objects.order_by('nombre').filter(trabajador=trabajador_login)
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
    investigacion = Investigacion.objects.filter(nombre=investigacion_nombre).first()
    participantes = Trabajador.objects.filter(investigacion=investigacion.id)

    context = {
        'Tareas': Tareas,
        'title': 'Gestor CFA',
        'section': 'Tareas',
        'investigacion_nombre': investigacion_nombre,
        'investigacion': investigacion,
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
        pass

    context = {
        'tarea_actual': tarea_actual,
        'participantes': participantes,
        'parte_de_horas': parte_de_horas,
        'parte_hora_form': parte_hora_form,
        'edicion': edicion,
        'trab': trab,
        'title': 'Gestor CFA',
        'section': tarea_actual.nombre,
    }
    return render(request, 'website/tarea.html', context)


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
@permission_required('models.change_investigacion')
@permission_required('models.add_investigacion')
def Crear_Investigacion(request):
    trabajador = Trabajador.objects.filter(usuario__username=request.user.username).first()
    if request.method == 'POST':
        Investigacion_From = CreacionInvestigacionForm(request.POST, trabajador=trabajador)
        if Investigacion_From.is_valid():
            Investigacion_From.save()
            investigacion = Investigacion.objects.filter(nombre=request.POST['nombre']).first()
            investigacion.trabajador.add(trabajador)
            return redirect('menu_investigaciones')
    else:
        Investigacion_From = CreacionInvestigacionForm(trabajador=trabajador)

    context = {
        'Investigacion_Form': Investigacion_From,
        'title': 'Gestor CFA',
        'section': 'Crear Investigacion',
    }
    return render(request, 'website/crear_investigacion.html', context)



@login_required()
@permission_required('models.change_investigacion')
@permission_required('models.add_investigacion')
def Editar_Investigacion(request, id_investigacion):
    investigacion = Investigacion.objects.filter(id=id_investigacion).first()
    trabajador = Trabajador.objects.filter(id=request.user.id).first()
    if request.method == 'POST':
        Edit_Investigacion_From = EdicionInvestigacionForm(request.POST, instance=investigacion, trabajador=trabajador, investigacion=investigacion)
        if Edit_Investigacion_From.is_valid():
            Edit_Investigacion_From.save()
            investigacion.trabajador.add(trabajador)
            trabajadores = Trabajador.objects.all()
            for trabajador in trabajadores:
                trabajador.horas()
            investigaciones = Investigacion.objects.all()
            for investigacion in investigaciones:
                tareas = Tarea.objects.filter(investigacion=investigacion)
                for tarea in tareas:
                    participantes = tarea.trabajador.all()
                    for participante in participantes:
                        if not investigacion.trabajador.filter(id=participante.id).first():
                            tarea.trabajador.remove(participante)

            return redirect('menu_investigaciones')
    else:
        Edit_Investigacion_From = EdicionInvestigacionForm(instance=investigacion, trabajador=trabajador, investigacion=investigacion)

    context = {
        'investigacion': investigacion,
        'Edit_Investigacion_Form': Edit_Investigacion_From,
        'title': 'Gestor CFA',
        'section': 'Editar Investigación',
    }
    return render(request, 'website/editar_investigacion.html', context)


@login_required()
@permission_required('models.add_tarea')
@permission_required('models.change_tarea')
def Crear_Tarea(request, investigacion_nombre):
    investigacion = Investigacion.objects.filter(nombre=investigacion_nombre).first()
    if request.method == 'POST':
        Tarea_From = CreacionTareaForm(request.POST, investigacion=investigacion)
        if Tarea_From.is_valid():
            tarea = Tarea_From.save()
            tarea.investigacion = investigacion
            tarea.save()
            return redirect('tarea_view', investigacion_nombre)
    else:
        Tarea_From = CreacionTareaForm(investigacion=investigacion)

    context = {
        'Tarea_Form': Tarea_From,
        'title': 'Gestor CFA',
        'section': 'Crear Tarea',
        'investigacion_nombre': investigacion_nombre,
        'investigacion': investigacion,
    }
    return render(request, 'website/crear_tarea.html', context)


@login_required()
@permission_required('models.change_tarea')
@permission_required('models.add_tarea')
def Editar_Tarea(request, id_tarea):
    tarea = Tarea.objects.get(id=id_tarea)
    if request.method == 'POST':
        Edit_Tarea_From = CreacionTareaForm(request.POST, investigacion=tarea.investigacion, instance=tarea)
        if Edit_Tarea_From.is_valid():
            Edit_Tarea_From.save()
            return redirect('tarea_view', tarea.investigacion)
    else:
        Edit_Tarea_From = CreacionTareaForm(instance=tarea, investigacion=tarea.investigacion)

    context = {
        'Edit_Tarea_Form': Edit_Tarea_From,
        'title': 'Gestor CFA',
        'section': 'Editar Tarea',
        'investigacion_nombre': tarea.investigacion,
        'investigacion': tarea.investigacion,
        'tarea': tarea,
    }
    return render(request, 'website/editar_tarea.html', context)


@login_required()
@permission_required('models.delete_investigacion')
@permission_required('models.delete_tarea')
def Eliminar_Tarea(request, tarea_id):
    tarea = Tarea.objects.filter(id=tarea_id).first()
    tarea.delete()
    return redirect('tarea_view', tarea.investigacion.nombre)


@login_required()
@permission_required('models.delete_investigacion')
@permission_required('models.delete_tarea')
def Eliminar_Investigacion(request, id_investigacion):
    investigacion = Investigacion.objects.filter(id=id_investigacion).first()
    investigacion.delete()
    return redirect('menu_investigaciones')


@login_required()
def Lista_Trabajadores(request):
    Trab = Trabajador.objects.order_by('nombre')

    context = {
        'Trab': Trab,
        'title': 'Gestor CFA',
        'section': 'Lista de Usuarios',
    }
    return render(request, 'website/trabajadores.html', context)



@login_required()
def Trabajador_Perfil(request, id_trabajador):
    trab = Trabajador.objects.filter(id=id_trabajador).first()
    user = User.objects.filter(trabajador=trab).first()
    investigaciones = Investigacion.objects.filter(trabajador=trab)
    tareas = Tarea.objects.filter(trabajador=trab)

    context = {
        'trab': trab,
        'user': user,
        'title': 'Gestor CFA',
        'section': trab.nombre,
        'investigaciones': investigaciones,
        'tareas': tareas,
    }
    return render(request, 'website/trabajador.html', context)













