from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from apps.usuarios.tokens import token_de_activiacion_cuenta
from django.core.mail import EmailMessage


def generar_mensaje(request, user, template):
    current_site = get_current_site(request)
    mensaje = render_to_string(template, {
        'user': user,
        'domain': current_site.domain,
        'uid': str(urlsafe_base64_encode(force_bytes(user.pk)))[2:-1],
        'token': token_de_activiacion_cuenta.make_token(user),
    })
    return mensaje


def enviar_mensaje_verificacion_correo(user, request, asunto='Activacion de tu cuenta ezPost'):
    asunto = asunto
    mensaje = generar_mensaje(request, user, 'usuario/email_activacion.html')
    user.email_user(asunto, mensaje)


def enviar_mensaje_confirmacion_correo(user, request, to_email):
    asunto = 'Confirmacion del correo electronico'
    mensaje = generar_mensaje(request, user, 'usuario/email_verificacion.html')
    email = EmailMessage(asunto, mensaje, to=[to_email])
    email.send()


def enviar_mensaje_restauracion_clave(user, request, to_email):
    asunto = 'Restauracion de la clave'
    mensaje = generar_mensaje(request, user, 'usuario/email_clave_restauracion.html')
    email = EmailMessage(asunto, mensaje, to=[to_email])
    email.send()
