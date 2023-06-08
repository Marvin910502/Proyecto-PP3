from core.models.models import *
from Gestor.inicial_data import *


def popualte_nomencladores():
    for institucion in instituciones_data:
        Institucion.objects.create(**institucion)
    for departamento in departamentos_data:
        Departamento.objects.create(**departamento)
    for nivel_academico in nivel_academico_data:
        Nivel_Academico.objects.create(**nivel_academico)
    for especializacion in especializacion_data:
        Especializacion.objects.create(**especializacion)


def populate_trabajadores():
    for usuario in usuarios_data:
        User.objects.create_user(**usuario)
    for trabajador in trabajador_data:
        Trabajador.objects.create(
            nombre=trabajador['nombre'],
            apellidos=trabajador['apellidos'],
            ci=trabajador['ci'],
            sexo=trabajador['sexo'],
            horas_ocupadas=0,
            institucion=Institucion.objects.filter(nombre=trabajador['institucion']).first(),
            departamento=Departamento.objects.filter(nombre=trabajador['departamento']).first(),
            nivel=Nivel_Academico.objects.filter(nivel_academico=trabajador['nivel_academico']).first(),
            especializacion=Especializacion.objects.filter(especializacion=trabajador['especializacion']).first(),
            usuario=User.objects.filter(username=trabajador['usuario']).first(),
        )


def populate_investigaciones():
    for investigacion in investigaciones_data:
        invest = Investigacion.objects.create(
            nombre=investigacion['nombre'],
            descripcion=investigacion['descripcion'],
            fecha_culminacion=investigacion['fecha_culminacion'],
            completado=investigacion['completado'],
        )
        invest.trabajador.add(Trabajador.objects.filter(nombre=investigacion['trabajador1']).first())
        invest.trabajador.add(Trabajador.objects.filter(nombre=investigacion['trabajador2']).first())
        if not investigacion['trabajador3'] == None:
            invest.trabajador.add(Trabajador.objects.filter(nombre=investigacion['trabajador3']).first())
    for investigacion in investigaciones_data:
        invest = Investigacion.objects.filter(nombre=investigacion['nombre']).first()
        invest.fecha_comienzo = investigacion['fecha_comienzo']
        invest.save()


def populate_tareas():
    for tarea in tarea_data:
        tar = Tarea.objects.create(
            nombre=tarea['nombre'],
            horas_necesarias=tarea['horas_necesarias'],
            descripcion=tarea['descripcion'],
            fecha_culminacion=tarea['fecha_culminacion'],
            investigacion=Investigacion.objects.filter(nombre=tarea['investigacion']).first()
        )
        if not tarea['trabajador1'] == None:
            tar.trabajador.add(Trabajador.objects.filter(nombre=tarea['trabajador1']).first())
        if not tarea['trabajador2'] == None:
            tar.trabajador.add(Trabajador.objects.filter(nombre=tarea['trabajador2']).first())
    for tarea in tarea_data:
        tar = Tarea.objects.filter(nombre=tarea['nombre']).first()
        tar.fecha_comienzo = tarea['fecha_comienzo']
        tar.save()
