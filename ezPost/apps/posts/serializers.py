from rest_framework.fields import  SerializerMethodField
from rest_framework.serializers import ModelSerializer,SlugRelatedField
from apps.posts.models import Post, TipoDenuncia, Aviso, Publicacion, PocketPost
from apps.usuarios.serializers import UsuarioDetalleSerializado


class TipoDenunciaSerializado(ModelSerializer):
    class Meta:
        model = TipoDenuncia
        fields = '__all__'


class PublicacionSerializada(ModelSerializer):
    autor = UsuarioDetalleSerializado()
    class Meta:
        model = Publicacion
        fields = ('pk', 'autor', 'fecha_creacion','post')


class PostDetalleSerializado(ModelSerializer):
    afinidad = SlugRelatedField(slug_field='nombre_afinidad', read_only=True)
    publicacion = PublicacionSerializada()
    visualizaciones = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('pk', 'titulo', 'portada', 'visualizaciones', 'afinidad', 'publicacion')

    def get_visualizaciones(self, obj):
        return obj.visualizacion_set.count()


class PostDetalleAviso(ModelSerializer):

    class Meta:
        model = Post
        fields = ('pk', 'titulo', 'portada')


class PocketPostDetalleAviso(ModelSerializer):
    class Meta:
        model = PocketPost
        fields = '__all__'


class PublicacionDetalleAviso(ModelSerializer):
    post = PostDetalleAviso()
    pocketpost = PocketPostDetalleAviso()

    class Meta:
        model = Publicacion
        fields = ('pk', 'fecha_creacion', 'post', 'tipo_publicacion', 'pocketpost')


class AvisoSerializado(ModelSerializer):
    publicacion = PublicacionDetalleAviso(many=False, read_only=True)
    
    class Meta:
        model = Aviso
        fields = '__all__'
