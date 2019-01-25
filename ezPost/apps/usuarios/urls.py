from django.urls import path
from apps.usuarios.views import *
from django.conf.urls import url


urlpatterns = [
    path('index',index_usuario,name="index_usuario"),
    path('account_activation_sent/', pedir_activacion_cuenta, name='pedir_activacion_cuenta'),
    url(r'^activar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activar_cuenta, name='activar'),
    path('signup/', signup, name='signup'),
    path('cuenta', mostrar_informacion_cuenta, name="mostrar_info"),
    path('actualizar', actualizar_perfil, name="actualizar"),
    path('reenviarmail', volver_enviar_correo_activacion, name='reenviar_mail'),
    path('cambiarclave', cambiar_clave, name='cambiar_clave'),
    url(r'^activarcorreo/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activar_correo, name='activar_correo'),
    path('cambiarcorreo', cambiar_email,name='cambiar_correo'),
    path('pedircorreo', pedir_verificacion_email, name='pedir_activacion_correo'),
    path('perfil/<pk>',MostrarInformacionUsuario.as_view(), name='ver_perfil')

]
