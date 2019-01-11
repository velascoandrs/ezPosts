from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from apps.usuarios.models import *
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Email')
    afinidades = forms.ModelMultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                queryset=Afinidad.objects.all()
    )
    fecha_nacimiento = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('fecha_nacimiento', 'first_name', 'last_name', 'username', 'email', 'afinidades')

    """
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con esa email")
        return email
    """


class UsuarioFormulario(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class PerfilUsuarioFormulario(ModelForm):
    class Meta:
        model = Perfil
        fields = ('foto_perfil', 'foto_perfil_portada', 'afinidades', 'fecha_nacimiento')

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioFormulario, self).__init__(*args, **kwargs)
        self.fields["afinidades"].widget = CheckboxSelectMultiple()
        self.fields["afinidades"].queryset = Afinidad.objects.all()


class CambiarEmailFormulario(forms.Form):
    email_nuevo = forms.EmailField(label="Email")

    def clean_email_nuevo(self):
        email = self.cleaned_data['email_nuevo']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con esa email")
        return email


class RestaurarCuentaFormulario(forms.Form):
    campo = forms.CharField(label="Escribe tu nombre de usuario o tu correo electronico")
    campo_es_correo = False

    def clean_campo(self):
        campo_valor = self.cleaned_data['campo']
        if User.objects.filter(email=campo_valor).exists():
            self.campo_es_correo = True
            return campo_valor
        if User.objects.filter(username=campo_valor).exists():
            self.campo_es_correo = False
            return campo_valor
        raise ValidationError('No existe un usuario con esa informacion!!')


class CambioClaveFormulario(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': "Las dos claves no coinciden",
    }
    new_password1 = forms.CharField(
        label="Nueva clave",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label= "Confirmacion de la nueva Clave",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
