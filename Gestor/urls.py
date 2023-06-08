"""Gestor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from core.gestion.views import *
from core.administrador.views import *
from django.contrib.auth import views as auth_views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('investigaciones/', Menu_Investigaciones, name='menu_investigaciones'),
    path('crear_usuario/', Crear_Usuario, name='crear_usuario'),
    path('eliminar_usuario/<int:id_user>', Eliminar_Usuario, name='eliminar_usuario'),
    path('menu_usuarios/', Lista_Usuarios, name='menu_usuarios'),
    path('editar_usuario/<int:id_user>/', Editar_Usuario, name='editar_usuario'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', Login, name='login'),
    path('menu_tareas/<str:investigacion_nombre>/', Tarea_View, name='tarea_view'),
    path('tarea/<str:tarea_nombre>/<str:nombre_usuario>', Tarea_Contenido, name='tarea_contenido'),
    path('crear_investigacion/', Crear_Investigacion, name='crear_investigacion'),
    path('crear_tarea/<str:investigacion_nombre>', Crear_Tarea, name='crear_tarea'),
    path('editar_investigacion/<int:id_investigacion>', Editar_Investigacion, name='editar_investigacion'),
    path('editar_tarea/<int:id_tarea>', Editar_Tarea, name='editar_tarea'),
    path('eliminar_tarea/<int:tarea_id>/', Eliminar_Tarea, name='eliminar_tarea'),
    path('eliminar_parte/<int:id_parte>/<str:tarea_nombre>', Eliminar_Parte, name='eliminar_parte'),
    path('editar_parte/<str:tarea_nombre>/<int:id_parte>', Editar_Parte, name='editar_parte'),
    path('trazas/', Trazas, name='trazas'),
    path('instituciones/', Instituciones, name='instituciones'),
    path('departamentos/', Departamentos, name='departamentos'),
    path('niveles_academicos/', Niveles_Academicos, name='niveles_academicos'),
    path('especializaciones/', Especializaciones, name='especializaciones'),
    path('eliminar_institucion/<int:id>', Eliminar_Institucion, name='eliminar_institucion'),
    path('eliminar_departamento/<int:id>', Eliminar_Departamento, name='eliminar_departamento'),
    path('eliminar_nivel_academico/<int:id>', Eliminar_Nivel_Academico, name='eliminar_nivel_academico'),
    path('eliminar_especializacion/<int:id>', Eliminar_Especializacion, name='eliminar_especializacion'),
]
