from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer,SlugRelatedField
from apps.posts.models import Post, TipoDenuncia, Aviso
from apps.usuarios.serializers import UsuarioDetalleSerializado


class TipoDenunciaSerializado(ModelSerializer):
    class Meta:
        model = TipoDenuncia
        fields = '__all__'


class PostDetalleSerializado(ModelSerializer):
    afinidad = SlugRelatedField(slug_field='nombre_afinidad', read_only=True)
    autor = UsuarioDetalleSerializado(many=False, read_only=True)
    visualizaciones = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('pk', 'titulo', 'portada', 'fecha_creacion','visualizaciones','afinidad', 'autor',)

    def get_visualizaciones(self, obj):
        return obj.visualizacion_set.count()


class AvisoSerializado(ModelSerializer):
    class Meta:
        model = Aviso
        fields = '__all__'
