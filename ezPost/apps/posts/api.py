# API DE AVISOS
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.posts.filters import PostFilter
from apps.posts.models import Aviso, Post, TipoDenuncia
from apps.posts.serializers import AvisoSerializado, PostDetalleSerializado, TipoDenunciaSerializado
from apps.usuarios.models import User


# Obtener los tipos de denuncia
class TipoDenunciaListApi(generics.ListAPIView):
    serializer_class = TipoDenunciaSerializado
    queryset = TipoDenuncia.objects.all()


class AvisoAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AvisoSerializado
    paginate_by = 3

    def get_queryset(self):
        queryset = Aviso.objects \
            .filter(publicacion__autor__id=self.request.user.id).order_by('-pk')
        return queryset


# API de POSTS v2, solamente muestra los detalles del POST no el contenido
class PostDetalleListApiv2(generics.ListAPIView):
    serializer_class = PostDetalleSerializado
    permission_classes = (AllowAny,)
    paginate_by = 10
    queryset = Post.objects.all().order_by('-pk')
    filter_class = PostFilter


# API de POSTS, solamente muestra los detalles del POST no el contenido
class PostDetalleListApi(generics.ListAPIView):
    serializer_class = PostDetalleSerializado
    permission_classes = (AllowAny,)
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-pk')
        titulo = self.request.query_params.get('titulo', None)
        autor_id = self.request.query_params.get('autor_id', None)

        # Si el usuario esta logeado filtrar los posts por las afinidades del usuario y los post creados por el mismo
        if self.request.user.is_authenticated and autor_id is None and titulo is None:
            usuario = User.objects.get(id=self.request.user.id)
            queryset = Post.objects\
                .filter(Q(afinidad__in=usuario.perfil.afinidades.all()) | Q(publicacion__autor=usuario)).order_by('-pk')

        if titulo is not None:
            queryset = queryset.filter(titulo__contains=titulo)
        if autor_id is not None:
            queryset = queryset.filter(publicacion__autor__id=autor_id)
        return queryset