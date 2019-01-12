from rest_framework.serializers import ModelSerializer, SlugRelatedField
from apps.usuarios.models import User,Perfil


class PerfilSerializado(ModelSerializer):
    afinidades = SlugRelatedField(slug_field='nombre_afinidad',many=True,read_only=True)

    class Meta:
        model = Perfil
        fields = ('foto_perfil', 'afinidades')


class UsuarioDetalleSerializado(ModelSerializer):
    perfil = PerfilSerializado(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'perfil')
