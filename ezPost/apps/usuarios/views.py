from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.contrib.auth import login, update_session_auth_hash
from django.http import HttpResponse
from apps.usuarios.models import User
from apps.usuarios.forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.usuarios.tokens import token_de_activiacion_cuenta
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.usuarios.helpers import *
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import DetailView
# Create your views here.


def index_usuario(request):
    return HttpResponse("Index de usuarios")


#  Vista que se encarga del registro de nuevos usuarios
def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # Obtener afinidades
            lista_afinidades = form.cleaned_data['afinidades']
            # Agregar al Perfil
            user.save()
            user.perfil.afinidades.set(lista_afinidades)
            user.perfil.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            user.perfil.save()
            # Guardar Perfil
            enviar_mensaje_verificacion_correo(user, request)
            print('Este es el id: {}'.format(user.id))
            request.session['id'] = user.id
            return redirect('usuarios:pedir_activacion_cuenta')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# Vista que renderiza el mensaje de confirmacion del email
def pedir_activacion_cuenta(request):
    return render(request, 'pedir_activacion_cuenta.html')


# Vista que renderiza el mensaje de confirmacion del email
def pedir_verificacion_email(request):
    return render(request, 'usuario/pedir_confirmacion_email.html')


# Vista que vuelve a enviar el correo de confrmacion del email
def volver_enviar_correo_activacion(request):

    if not request.user.is_authenticated:
        uid = request.session.get('id')
        if uid:
            user = User.objects.get(pk=uid)
        else:
            return redirect('/')
    else:
        user = request.user
    if not user.perfil.email_esta_confirmado:
        enviar_mensaje_verificacion_correo(user, request)
        return redirect('usuarios:pedir_activacion_cuenta')
    else:
        return render(request, 'activacion_cuenta_invalida.html')


# Vista que activa la cuenta del usuario recibe como parametro el token de activacion y el uid
def activar_cuenta(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uidb64)
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_de_activiacion_cuenta.check_token(user, token):
        user.is_active = True
        user.perfil.email_esta_confirmado = True
        user.save()
        request.session.pop('id')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return render(request, 'activacion_cuenta_invalida.html')


@login_required(login_url='/')
@transaction.atomic
def actualizar_perfil(request):
    if request.method == 'POST':
        formulario_usuario = UsuarioFormulario(request.POST, instance=request.user)
        formulario_perfil = PerfilUsuarioFormulario(request.POST, request.FILES, instance=request.user.perfil)
        if formulario_usuario.is_valid() and formulario_perfil.is_valid():
            formulario_usuario.save()
            formulario_perfil.save(commit=False)
            formulario_perfil.save_m2m()
            messages.success(request, 'Tu perfil fue actualizado exitosamente')
            return redirect('usuarios:mostrar_info')
        else:
            messages.error(request, 'Por favor corriga los siguiente errores')
    else:
        formulario_usuario = UsuarioFormulario(instance=request.user)
        formulario_perfil = PerfilUsuarioFormulario(instance=request.user.perfil)

    return render(request, 'usuario/perfil.html', {
        'formulario_usuario': formulario_usuario,
        'formulario_perfil': formulario_perfil
    }
                  )


# Vista que muestra la informacion del usuario
@login_required(login_url='/')
def mostrar_informacion_cuenta(request):
    return render(request, 'usuario/informacion_cuenta.html')


# Vista que muestra el perfil de los usuarios
class MostrarInformacionUsuario(DetailView):
    model = User
    template_name = 'usuario/informacion_cuenta.html'
    context_object_name = "usuario"


# Cambiar clave
@login_required(login_url='/')
def cambiar_clave(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Clave actualizada exitosamente!')
            return redirect('usuarios:cambiar_clave')
        else:
            messages.error(request, 'Corriga los siguientes errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuario/cambiar_clave.html', {
        'form': form
    })


# Cambiar Email
@login_required(login_url='/')
def cambiar_email(request):
    if request.method == 'POST':
        form = CambiarEmailFormulario(request.user,request.POST)
        if form.is_valid():
            nuevo_correo = form.cleaned_data['email_nuevo']
            enviar_mensaje_confirmacion_correo(request.user, request, nuevo_correo)
            request.session['nuevo_email'] = nuevo_correo
            return redirect('usuarios:pedir_activacion_correo')
    else:
        form = CambiarEmailFormulario(request.user)
    return render(request, 'usuario/cambiar_email.html', {'form': form})


# Vista que activa el nuevo correo del usuario recibe como parametro el token de activacion y el uid
@login_required(login_url='/')
def activar_correo(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uidb64)
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_de_activiacion_cuenta.check_token(user, token):
        user.email = request.session.get('nuevo_email')
        user.save()
        request.session.pop('nuevo_email')
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'activacion_cuenta_invalida.html')