from rest_framework.fields import ReadOnlyField
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer,SlugRelatedField
from apps.posts.models import Post
from apps.usuarios.serializers import UsuarioDetalleSerializado


class PostDetalleSerializado(ModelSerializer):
    #autor = SlugRelatedField(slug_field='username', read_only=True)
    afinidad = SlugRelatedField(slug_field='nombre_afinidad', read_only=True)
    autor = UsuarioDetalleSerializado(many=False, read_only=True)

    class Meta:
        model = Post
        #fields = ('pk', 'titulo', 'portada', 'autor','autor_id','afinidad')
        fields = ('pk', 'titulo', 'portada', 'fecha_creacion', 'afinidad', 'autor')
