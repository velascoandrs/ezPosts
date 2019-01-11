from rest_framework.serializers import ModelSerializer,SlugRelatedField
from apps.posts.models import Post


class PostDetalleSerializado(ModelSerializer):
    autor = SlugRelatedField(slug_field='username', read_only=True)
    autor.pk = SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'titulo', 'portada', 'autor')
