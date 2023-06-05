# Generated by Django 4.1.3 on 2023-02-05 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Departamento')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'Departamento',
            },
        ),
        migrations.CreateModel(
            name='Especializacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Especielización',
                'verbose_name_plural': 'Especielizaciones',
                'db_table': 'Especialización',
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Evento')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha_comienzo', models.DateTimeField(verbose_name='Fecha de Inicio')),
                ('fecha_culminacion', models.DateTimeField(verbose_name='Fecha de Culminación')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'Evento',
            },
        ),
        migrations.CreateModel(
            name='Informe_Final_Resultados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=50, null=True, verbose_name='Nombre del Proyecto')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Informe Final de Resultados',
                'verbose_name_plural': 'Informes Finales de Resultados',
                'db_table': 'Informe Final de Resultados',
            },
        ),
        migrations.CreateModel(
            name='Informe_Semestral_Resultados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=50, null=True, verbose_name='Nombre del Proyecto')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Informe Semestral de Resultados',
                'verbose_name_plural': 'Informes Semestrales de Resultados',
                'db_table': 'Informe Semestral Resultados',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de Institución')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('direccion', models.CharField(max_length=50, verbose_name='Direccion de la Institución')),
            ],
            options={
                'verbose_name': 'Institucion',
                'verbose_name_plural': 'Instituciones',
                'db_table': 'Institución',
            },
        ),
        migrations.CreateModel(
            name='Investigacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Investigación')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha_comienzo', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Inicio')),
                ('fecha_culminacion', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Culminación')),
                ('completado', models.IntegerField(blank=True, default=0, null=True, verbose_name='Porciento completado')),
                ('activo', models.BooleanField(default=False, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Investigación',
                'verbose_name_plural': 'Investigaciones',
                'db_table': 'Investigación',
            },
        ),
        migrations.CreateModel(
            name='Nivel_Academico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_academico', models.CharField(max_length=50, verbose_name='Nivel Académico')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Nivel Academico',
                'verbose_name_plural': 'Niveles Academicos',
                'db_table': 'Nivel Académico',
            },
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Publicación')),
                ('fecha', models.DateTimeField(verbose_name='Fecha de Publicación')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('investigacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.investigacion', verbose_name='Investigación')),
            ],
            options={
                'verbose_name': 'Publicación',
                'verbose_name_plural': 'Publicaciones',
                'db_table': 'Publicación',
            },
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre')),
                ('apellidos', models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellidos')),
                ('ci', models.CharField(max_length=11, verbose_name='Carnet de Identidad')),
                ('sexo', models.CharField(choices=[('Masculino', 'masculino'), ('Femenino', 'femenino'), ('Otro', 'otro')], max_length=50, verbose_name='Sexo')),
                ('horas_ocupadas', models.IntegerField(default=0, verbose_name='Horas Ocupadas')),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.departamento', verbose_name='Departamento')),
                ('especializacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.especializacion', verbose_name='Especialización')),
                ('institucion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.institucion', verbose_name='Institución')),
                ('nivel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.nivel_academico', verbose_name='Nivel Académico')),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Trabajador',
                'verbose_name_plural': 'Trabajadores',
                'db_table': 'Trabajador',
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Tarea')),
                ('horas_necesarias', models.IntegerField(verbose_name='Cantidad de Horas Necesarias')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha_comienzo', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de Inicio')),
                ('fecha_culminacion', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Culminación')),
                ('evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.evento', verbose_name='Evento')),
                ('informe_final', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.informe_final_resultados', verbose_name='Informe Final de Resultados')),
                ('informe_sem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.informe_semestral_resultados', verbose_name='Informe Semestral de Resultados')),
                ('investigacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.investigacion', verbose_name='Investigación')),
                ('publicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.publicacion', verbose_name='Publicación')),
                ('trabajador', models.ManyToManyField(blank=True, related_name='tarea', to='models.trabajador', verbose_name='Trabajador')),
            ],
            options={
                'verbose_name': 'Tarea',
                'verbose_name_plural': 'Tareas',
                'db_table': 'Tarea',
            },
        ),
        migrations.CreateModel(
            name='Parte_Hora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
                ('fecha', models.DateField(auto_now=True, null=True, verbose_name='Fecha')),
                ('horas_dedicadas', models.IntegerField(verbose_name='Horas Dedicadas')),
                ('tarea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.tarea', verbose_name='Tarea')),
                ('trabajador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.trabajador', verbose_name='Trabajador')),
            ],
            options={
                'verbose_name': 'Parte de Hora',
                'verbose_name_plural': 'Parte de Horas',
                'db_table': 'Parte de Hora',
            },
        ),
        migrations.AddField(
            model_name='investigacion',
            name='trabajador',
            field=models.ManyToManyField(blank=True, related_name='investigacion', to='models.trabajador', verbose_name='Trabajador'),
        ),
        migrations.AddField(
            model_name='informe_semestral_resultados',
            name='investigacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.investigacion', verbose_name='Investigación'),
        ),
        migrations.AddField(
            model_name='informe_final_resultados',
            name='investigacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.investigacion', verbose_name='Investigación'),
        ),
        migrations.AddField(
            model_name='evento',
            name='investigacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='models.investigacion', verbose_name='Investigación'),
        ),
    ]
