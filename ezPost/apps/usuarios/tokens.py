from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


# Clase que genera un token para la activacion de la cuenta de usuario
class GeneradorTokenActivacionCuenta(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.perfil.email_esta_confirmado)
        )


token_de_activiacion_cuenta = GeneradorTokenActivacionCuenta()