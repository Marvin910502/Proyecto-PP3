from django.shortcuts import render, redirect
from django.contrib.auth import *
from core.models.models import *
from django.contrib.auth.decorators import *
from hmac import compare_digest
from Gestor.globals import SUCCESS_MESSAGE, DANGER_MESSAGE, WARNING_MESSAGE

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
    message, class_alert = check_session_message(request)

    password = ''
    password2 = ''
    username = ''
    nombre = ''
    apellidos = ''
    ci = ''
    sexo = ''
    institucion = ''
    departamento = ''
    nivel = ''
    especializacion = ''
    horas_ocupadas = ''
    if request.method == 'POST':
        request_post = request.POST
        password = request_post.get('contraseña')
        password2 = request_post.get('confirmar_contraseña')
        username = request_post.get('username')
        nombre = request_post.get('nombre')
        apellidos = request_post.get('apellidos')
        ci = request_post.get('ci')
        sexo = request_post.get('sexo')
        institucion = Institucion.objects.filter(id=request_post.get('institucion')).first()
        departamento = Departamento.objects.filter(id=request_post.get('departamento')).first()
        nivel = Nivel_Academico.objects.filter(id=request_post.get('nivel_academico')).first()
        especializacion = Especializacion.objects.filter(id=request_post.get('especializacion')).first()
        horas_ocupadas = 0
        if compare_digest(password, password2):
            usuario = User.objects.create_user(
                username=username,
                password=password,
            )
            Trabajador.objects.create(
                nombre=nombre,
                apellidos=apellidos,
                ci=ci,
                sexo=sexo,
                institucion=institucion,
                departamento=departamento,
                nivel=nivel,
                especializacion=especializacion,
                horas_ocupadas=horas_ocupadas,
                usuario=usuario,
            )
            return redirect('menu_usuarios')
        else:
            message = ("Las contraseñas no coenciden.")
            class_alert = DANGER_MESSAGE

    institucion_list = Institucion.objects.all()
    departamento_list = Departamento.objects.all()
    nivel_list = Nivel_Academico.objects.all()
    especializacion_list = Especializacion.objects.all()
    context = {
        'nombre': nombre,
        'apellidos': apellidos,
        'ci': ci,
        'sexo': sexo,
        'institucion_id': institucion,
        'departamento_id': departamento,
        'nivel_id': nivel,
        'especializacion_id': especializacion,
        'horas_ocupadas': horas_ocupadas,
        'username': username,
        'password': password,
        'password2': password2,
        'message': message,
        'class_alert': class_alert,
        'institucion_list': institucion_list,
        'departamento_list': departamento_list,
        'nivel_list': nivel_list,
        'especializacion_list': especializacion_list,
    }

    return render(request, 'admin/crear_usuario.html', context)


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


def check_session_message(request):
    if 'message' in request.session and 'class_alert' in request.session:
        message, class_alert = request.session.get('message'), request.session.get('class_alert')
        del request.session['message']
        del request.session['class_alert']
        return message, class_alert
    else:
        return None, None