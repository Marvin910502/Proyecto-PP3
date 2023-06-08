from django.shortcuts import render, redirect
from django.contrib.auth import *
from core.models.models import *
from django.contrib.auth.decorators import *
from hmac import compare_digest
from Gestor.globals import SUCCESS_MESSAGE, DANGER_MESSAGE, WARNING_MESSAGE
from auditlog.models import *

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
    permisos = Permission.objects.all()

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
            if not User.objects.filter(username=username).first() and not Trabajador.objects.filter(ci=ci).first():
                if len(ci) == 11 and ci.isnumeric():
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

                    for permiso in permisos:
                        if str(permiso.id) in request_post:
                            usuario.user_permissions.add(permiso)

                    return redirect('menu_usuarios')
                else:
                    message = ("El carnet de identidad tiene que tener 11 dígitos y solo números.")
                    class_alert = DANGER_MESSAGE
            else:
                message = ("El usuario que intenta crear ya existe.")
                class_alert = DANGER_MESSAGE
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
        'title': 'Gestor CFA',
        'section': 'Crear Usuario',
        'permisos': permisos,
    }

    return render(request, 'admin/crear_usuario.html', context)


def Eliminar_Usuario(request, id_user):
    usuario = User.objects.filter(id=id_user).first()
    trabajador = Trabajador.objects.filter(usuario_id=id_user).first()
    usuario.delete()
    trabajador.delete()
    return redirect('menu_usuarios')


@login_required()
def Editar_Usuario(request, id_user):
    message, class_alert = check_session_message(request)
    permisos = Permission.objects.all()

    trabajador = Trabajador.objects.filter(usuario_id=id_user).first()

    usuario = User.objects.filter(id=id_user).first()
    password = ''
    password2 = ''
    old_password = ''
    username = usuario.username
    nombre = trabajador.nombre
    apellidos = trabajador.apellidos
    ci = trabajador.ci
    sexo = trabajador.sexo
    institucion = trabajador.institucion
    departamento = trabajador.departamento
    nivel = trabajador.nivel
    especializacion = trabajador.especializacion
    horas_ocupadas = trabajador.horas_ocupadas
    if request.method == 'POST':
        request_post = request.POST
        if 'editar_usuario' in request_post:
            username = request_post.get('username')
            nombre = request_post.get('nombre')
            apellidos = request_post.get('apellidos')
            ci = request_post.get('ci')
            sexo = request_post.get('sexo')
            institucion = Institucion.objects.filter(id=request_post.get('institucion')).first()
            departamento = Departamento.objects.filter(id=request_post.get('departamento')).first()
            nivel = Nivel_Academico.objects.filter(id=request_post.get('nivel_academico')).first()
            especializacion = Especializacion.objects.filter(id=request_post.get('especializacion')).first()
            if not User.objects.filter(username=username).exclude(id=usuario.id).first() and not Trabajador.objects.filter(ci=ci).exclude(id=trabajador.id).first():
                if len(ci) == 11 and ci.isnumeric():
                    usuario.username = username
                    usuario.save()
                    trabajador.nombre = nombre
                    trabajador.apellidos = apellidos
                    trabajador.ci = ci
                    trabajador.sexo = sexo
                    trabajador.institucion = institucion
                    trabajador.departamento = departamento
                    trabajador.nivel = nivel
                    trabajador.especializacion = especializacion
                    trabajador.save()

                    for permiso in permisos:
                        if str(permiso.id) in request_post:
                            usuario.user_permissions.add(permiso)
                        else:
                            usuario.user_permissions.remove(permiso)

                else:
                    message = ("El carnet de identidad tiene que tener 11 dígitos y solo números.")
                    class_alert = DANGER_MESSAGE
            else:
                message = ("El nombre de usuario o el carnet que editó ya existen.")
                class_alert = DANGER_MESSAGE

        elif 'cambiar_contraseña' in request_post:
            password = request_post.get('contraseña')
            password2 = request_post.get('confirmar_contraseña')
            old_password = request_post.get('contraseña_vieja')
            if authenticate(username=usuario.username, password=old_password):
                if compare_digest(password, password2):
                    usuario.set_password(password)
                    usuario.save()
                else:
                    message = ("La contraseñas nuevas no coenciden.")
                    class_alert = DANGER_MESSAGE
            else:
                message = ("La contraseña actual es incorrecta.")
                class_alert = DANGER_MESSAGE

    institucion_list = Institucion.objects.all()
    departamento_list = Departamento.objects.all()
    nivel_list = Nivel_Academico.objects.all()
    especializacion_list = Especializacion.objects.all()
    permisos_aplicados = Permission.objects.filter(user=usuario)
    permisos_list = []
    for permiso in permisos_aplicados:
        permisos_list.append(permiso.id)

    context = {
        'usuario': usuario,
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
        'old_password': old_password,
        'title': 'Gestor CFA',
        'section': 'Editar Usuario',
        'permisos': permisos,
        'permisos_list': permisos_list,
    }

    return render(request, 'admin/editar_usuario.html', context)


@login_required()
def Lista_Usuarios(request):
    Trab = Trabajador.objects.order_by('nombre')

    context = {
        'Trab': Trab,
        'title': 'Gestor CFA',
        'section': 'Lista de Usuarios',
    }
    return render(request, 'admin/menu_usuarios.html', context)


def check_session_message(request):
    if 'message' in request.session and 'class_alert' in request.session:
        message, class_alert = request.session.get('message'), request.session.get('class_alert')
        del request.session['message']
        del request.session['class_alert']
        return message, class_alert
    else:
        return None, None


def Trazas(request):
    trazas = LogEntry.objects.all()

    context = {
        "trazas": trazas,
        "title": 'Gestor CFA',
        "section": 'Trazas'
    }
    return render(request, 'admin/trazas.html', context)