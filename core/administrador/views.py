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
@permission_required('auth.add_user')
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


@login_required()
@permission_required('auth.delete_user')
def Eliminar_Usuario(request, id_user):
    usuario = User.objects.filter(id=id_user).first()
    trabajador = Trabajador.objects.filter(usuario_id=id_user).first()
    usuario.delete()
    trabajador.delete()
    return redirect('menu_usuarios')


@login_required()
@permission_required('auth.change_user')
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
@permission_required('auth.change_user')
@permission_required('auth.delete_user')
@permission_required('auth.add_user')
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


@login_required()
@permission_required('admin.view_logentry')
def Trazas(request):
    trazas = LogEntry.objects.all()

    context = {
        "trazas": trazas,
        "title": 'Gestor CFA',
        "section": 'Trazas'
    }
    return render(request, 'admin/trazas.html', context)


@login_required()
@permission_required('models.add_institucion')
@permission_required('models.change_institucion')
def Instituciones(request):
    instituciones = Institucion.objects.all().order_by('nombre')

    if request.method == 'POST':
        request_post = request.POST
        if 'crear_institucion' in request_post:
            Institucion.objects.create(
                nombre=request_post.get('nombre'),
                descripcion=request_post.get('descripcion'),
                direccion=request_post.get('direccion'),
            )
        elif 'editar_institucion' in request_post:
            institucion = Institucion.objects.filter(id=request_post.get('editar_institucion')).first()
            institucion.nombre = request_post.get('nombre')
            institucion.descripcion = request_post.get('descripcion')
            institucion.direccion = request_post.get('direccion')
            institucion.save()

    context = {
        "instituciones": instituciones,
        "title": 'Gestor CFA',
        "section": 'Instituciones',
    }
    return render(request, 'admin/instituciones.html', context)


@login_required()
@permission_required('models.add_departamento')
@permission_required('models.change_departamento')
def Departamentos(request):
    departamentos = Departamento.objects.all().order_by('nombre')

    if request.method == 'POST':
        request_post = request.POST
        if 'crear_departamento' in request_post:
            Departamento.objects.create(
                nombre=request_post.get('nombre'),
                descripcion=request_post.get('descripcion'),
            )
        elif 'editar_departamento' in request_post:
            departamento = Departamento.objects.filter(id=request_post.get('editar_departamento')).first()
            departamento.nombre = request_post.get('nombre')
            departamento.descripcion = request_post.get('descripcion')
            departamento.save()

    context = {
        "departamentos": departamentos,
        "title": 'Gestor CFA',
        "section": 'Departamentos',
    }
    return render(request, 'admin/departamentos.html', context)


@login_required()
@permission_required('models.add_nivel_academico')
@permission_required('models.change_nivel_academico')
def Niveles_Academicos(request):
    niveles_academicos = Nivel_Academico.objects.all().order_by('nivel_academico')

    if request.method == 'POST':
        request_post = request.POST
        if 'crear_nivel_academico' in request_post:
            Nivel_Academico.objects.create(
                nivel_academico=request_post.get('nombre'),
                descripcion=request_post.get('descripcion'),
            )
        elif 'editar_nivel_academico' in request_post:
            nivel_academico = Nivel_Academico.objects.filter(id=request_post.get('editar_nivel_academico')).first()
            nivel_academico.nivel_academico = request_post.get('nombre')
            nivel_academico.descripcion = request_post.get('descripcion')
            nivel_academico.save()

    context = {
        "niveles_academicos": niveles_academicos,
        "title": 'Gestor CFA',
        "section": 'Niveles Académicos',
    }
    return render(request, 'admin/nivel_academico.html', context)


@login_required()
@permission_required('models.add_especializacion')
@permission_required('models.change_especializacion')
def Especializaciones(request):
    especializaciones = Especializacion.objects.all().order_by('especializacion')

    if request.method == 'POST':
        request_post = request.POST
        if 'crear_especializacion' in request_post:
            Especializacion.objects.create(
                especializacion=request_post.get('nombre'),
                descripcion=request_post.get('descripcion'),
            )
        elif 'editar_especializacion' in request_post:
            especializacion = Especializacion.objects.filter(id=request_post.get('editar_especializacion')).first()
            especializacion.nivel_academico = request_post.get('nombre')
            especializacion.descripcion = request_post.get('descripcion')
            especializacion.save()

    context = {
        "especializaciones": especializaciones,
        "title": 'Gestor CFA',
        "section": 'Especializaciones',
    }
    return render(request, 'admin/especializaciones.html', context)


@login_required()
@permission_required('models.delete_institucion')
def Eliminar_Institucion(request, id):
    institucion = Institucion.objects.filter(id=id).first()
    institucion.delete()
    return redirect('instituciones')


@login_required()
@permission_required('models.delete_departamento')
def Eliminar_Departamento(request, id):
    departamento = Departamento.objects.filter(id=id).first()
    departamento.delete()
    return redirect('departamentos')


@login_required()
@permission_required('models.delete_nivel_academico')
def Eliminar_Nivel_Academico(request, id):
    nivel_academico = Nivel_Academico.objects.filter(id=id).first()
    nivel_academico.delete()
    return redirect('niveles_academicos')


@login_required()
@permission_required('models.delete_especializacion')
def Eliminar_Especializacion(request, id):
    especializacion = Especializacion.objects.filter(id=id).first()
    especializacion.delete()
    return redirect('especializaciones')
