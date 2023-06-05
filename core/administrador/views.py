from django.shortcuts import render, redirect
from django.contrib.auth import *
from core.models.models import *
from django.contrib.auth.decorators import *

# Create your views here.


def Login(request):
    if request.method == 'POST':
        request_post = request.POST
        usuario = User.objects.filter(username=request_post.get('username')).first()
        if authenticate(username=usuario.username, password=request_post.get('password')):
            login(request, usuario)
            return redirect('menu_investigaciones')

    context = {
        "title": "Gestor de Proyectos CFA"
    }
    return render(request, 'admin/login.html', context)

@login_required()
def Crear_Usuario(request):
    if request.method == 'POST':

        if Usuario_Form.is_valid() and Trabajador_Form.is_valid():
            usuario =  Usuario_Form.save()
            trabajador = Trabajador_Form.save(commit=False)          
            trabajador.usuario = usuario
            trabajador.save()
            return redirect('menu_usuarios')
    else:
        Usuario_Form = CreacionUsuarioForm()
        Trabajador_Form = CrearTrabajadorForm()
    return render(request, 'admin/crear_usuario.html', {'Usuario_Form': Usuario_Form, 'Trabajador_Form': Trabajador_Form})


@login_required()
def Editar_Usuario(request, id_user):
    user = User.objects.get(id = id_user)
    trab = Trabajador.objects.filter(usuario = user).first()
    if request.method == 'POST':
        Usuario_Form = EditarUsuarioForm(request.POST, instance = user)
        Trabajador_Form = EditarTrabajadorForm(request.POST, instance = trab)
        if Usuario_Form.is_valid() and Trabajador_Form.is_valid():
            usuario =  Usuario_Form.save()
            trabajador = Trabajador_Form.save(commit=False)          
            trabajador.usuario = usuario
            trabajador.save()
            return redirect('home')
    else:
        Usuario_Form = EditarUsuarioForm(instance = user)
        Trabajador_Form = EditarTrabajadorForm(instance = trab)
    return render(request, 'admin/editar_usuario.html', {'Usuario_Form': Usuario_Form, 'Trabajador_Form': Trabajador_Form, 'id_user': id_user})


@login_required()
def Usaurio(request, id_user):
    user = User.objects.get(id=id_user)
    trab = Trabajador.objects.filter(usuario = user).first()    
    return render(request, 'website/../../templates/admin/perfil.html', {'trab': trab})


@login_required()
def Lista_Usuarios(request):
    Trab = Trabajador.objects.order_by('nombre')
    return render(request, 'website/../../templates/admin/menu_usuarios.html', {'Trab': Trab})