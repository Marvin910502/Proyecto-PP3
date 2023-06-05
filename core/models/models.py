from django.db import models
from django.contrib.auth.models import *

# Create your models here.


class Institucion(models.Model):

    nombre = models.CharField(verbose_name='Nombre de Institución', max_length=50)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    direccion = models.CharField(verbose_name='Direccion de la Institución', max_length=50)


    class Meta:
        verbose_name = "Institucion"
        verbose_name_plural = "Instituciones"
        db_table = "Institución"

    def __str__(self):
        return self.nombre


class Departamento(models.Model):

    nombre = models.CharField(verbose_name='Nombre Departamento', max_length=50) 
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)  
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "Departamento"

    def __str__(self):
        return self.nombre


class Nivel_Academico(models.Model):

    nivel_academico = models.CharField(verbose_name='Nivel Académico', max_length=50) 
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)  

    class Meta:
        verbose_name = "Nivel Academico"
        verbose_name_plural = "Niveles Academicos"
        db_table = "Nivel Académico"

    def __str__(self):
        return self.nivel_academico


class Especializacion(models.Model):

    especializacion = models.CharField(verbose_name='Especialización', max_length=50, null=True, blank=True) 
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)  

    class Meta:
        verbose_name = "Especielización"
        verbose_name_plural = "Especielizaciones"
        db_table = "Especialización"

    def __str__(self):
        return self.especializacion


class Investigacion(models.Model):

    nombre = models.CharField(verbose_name='Nombre Investigación', max_length=50) 
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fecha_comienzo = models.DateTimeField(verbose_name='Fecha de Inicio', auto_now=False, auto_now_add=True, null=True, blank=True)
    fecha_culminacion = models.DateTimeField(verbose_name='Fecha de Culminación' , auto_now=False, auto_now_add=False, null=True, blank=True)  
    completado = models.IntegerField(verbose_name='Porciento completado', null=True, blank=True, default=0)
    trabajador = models.ManyToManyField('Trabajador', verbose_name='Trabajador', related_name='investigacion', blank=True)
    activo = models.BooleanField(verbose_name='Activo', default=False)
    
    class Meta:
        verbose_name = "Investigación"
        verbose_name_plural = "Investigaciones"
        db_table = "Investigación"

    def __str__(self):
        return self.nombre


class Evento(models.Model):

    nombre = models.CharField(verbose_name='Nombre Evento', max_length=50) 
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fecha_comienzo = models.DateTimeField(verbose_name='Fecha de Inicio', auto_now=False, auto_now_add=False)
    fecha_culminacion = models.DateTimeField(verbose_name='Fecha de Culminación' , auto_now=False, auto_now_add=False)  
    investigacion = models.ForeignKey('Investigacion', verbose_name='Investigación', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        db_table = "Evento"

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):

    nombre = models.CharField(verbose_name='Nombre Publicación', max_length=50) 
    fecha = models.DateTimeField(verbose_name='Fecha de Publicación', auto_now=False, auto_now_add=False)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    investigacion = models.ForeignKey('Investigacion', verbose_name='Investigación', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        db_table = "Publicación"

    def __str__(self):
        return self.nombre


class Informe_Semestral_Resultados(models.Model):

    nombre_proyecto = models.CharField(verbose_name='Nombre del Proyecto', max_length=50, null=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fecha = models.DateTimeField(verbose_name='Fecha', auto_now=False, auto_now_add=False)
    investigacion = models.ForeignKey('Investigacion', verbose_name='Investigación', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = "Informe Semestral de Resultados"
        verbose_name_plural = "Informes Semestrales de Resultados"
        db_table = "Informe Semestral Resultados"

    def __int__(self):
        return self.id


class Informe_Final_Resultados(models.Model):

    nombre_proyecto = models.CharField(verbose_name='Nombre del Proyecto', max_length=50, null=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fecha = models.DateTimeField(verbose_name='Fecha', auto_now=False, auto_now_add=False)
    investigacion = models.ForeignKey('Investigacion', verbose_name='Investigación', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = "Informe Final de Resultados"
        verbose_name_plural = "Informes Finales de Resultados"
        db_table = "Informe Final de Resultados"

    def __int__(self):
        return self.id


class Trabajador(models.Model):

    SEXO = [
    ('Masculino', 'masculino'),
    ('Femenino', 'femenino'),
    ('Otro', 'otro'),
    ]


    nombre = models.CharField(verbose_name= 'Nombre', max_length=50, null=True, blank=True)
    apellidos = models.CharField(verbose_name='Apellidos', max_length=100, null=True, blank=True)
    ci = models.CharField(verbose_name='Carnet de Identidad', max_length=11)
    sexo = models.CharField(verbose_name='Sexo', max_length=50, choices=SEXO)
    horas_ocupadas = models.IntegerField(verbose_name='Horas Ocupadas', default=0)
    departamento = models.ForeignKey('Departamento', verbose_name='Departamento', on_delete=models.DO_NOTHING, null=True, blank=True)
    nivel = models.ForeignKey('Nivel_Academico', verbose_name='Nivel Académico', on_delete=models.DO_NOTHING, null=True, blank=True)
    institucion = models.ForeignKey('Institucion', verbose_name='Institución', on_delete=models.DO_NOTHING, null=True, blank=True)
    especializacion = models.ForeignKey("Especializacion", verbose_name='Especialización', on_delete=models.DO_NOTHING, null=True, blank=True)
    usuario = models.OneToOneField(User, verbose_name='Usuario', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        db_table = "Trabajador"

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'


class Parte_Hora(models.Model):

    tarea = models.ForeignKey("Tarea", verbose_name='Tarea', on_delete=models.CASCADE, null=True, blank=True)
    trabajador = models.ForeignKey("Trabajador", verbose_name='Trabajador', on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(verbose_name='Descripcion', null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha', auto_now=False, auto_now_add=False, null=True, blank=True)
    horas_dedicadas = models.IntegerField(verbose_name='Horas Dedicadas')

    class Meta:
        verbose_name = 'Parte de Hora'
        verbose_name_plural = 'Parte de Horas'
        db_table = "Parte de Hora"

    def __int__(self):
        return self.id


class Tarea(models.Model):

    nombre = models.CharField(verbose_name='Nombre Tarea', max_length=50) 
    horas_necesarias = models.IntegerField(verbose_name='Cantidad de Horas Necesarias')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    investigacion = models.ForeignKey("Investigacion", verbose_name='Investigación', on_delete=models.CASCADE, null=True, blank=True)
    evento = models.ForeignKey("Evento", verbose_name='Evento', on_delete=models.CASCADE, null=True, blank=True)
    publicacion = models.ForeignKey("Publicacion", verbose_name='Publicación', on_delete=models.CASCADE, null=True, blank=True)
    informe_sem = models.ForeignKey("Informe_Semestral_Resultados", verbose_name='Informe Semestral de Resultados', on_delete=models.CASCADE, null=True, blank=True)
    informe_final = models.ForeignKey("Informe_Final_Resultados", verbose_name='Informe Final de Resultados', on_delete=models.CASCADE, null=True, blank=True)
    fecha_comienzo = models.DateTimeField(verbose_name='Fecha de Inicio', auto_now=False, auto_now_add=True, null=True, blank=True)
    fecha_culminacion = models.DateTimeField(verbose_name='Fecha de Culminación' , auto_now=False, auto_now_add=False, null=True, blank=True)  
    trabajador = models.ManyToManyField(Trabajador,verbose_name='Trabajador', blank=True, related_name='tarea')

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        db_table = "Tarea"

    def __str__(self):
        return self.nombre


class Permiso(models.Model):

    nombre = models.CharField(verbose_name='Nombre Tarea', max_length=50)
    usuario = models.ManyToManyField(User, verbose_name='Usuario', blank=True, null=True, related_name='user')

    class Meta:
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        db_table = "Permiso"

    def __str__(self):
        return self.nombre









