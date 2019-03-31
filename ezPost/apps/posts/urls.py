from django.urls import path
from apps.posts.views import *
from apps.posts.api import *

urlpatterns = [
    path('index', index_post, name='index_post'),
    path('crearPost', crear_post, name='crear_post'),
    path('api/post', PostDetalleListApi.as_view(), name='post_list'),
    path('api/v2/post', PostDetalleListApiv2.as_view(),name='post_list_v2'),
    path('actualizar/<int:post_id>/', editar_post, name='editar_post'),
    path('eliminar/<int:post_id>/', eliminar_post, name='eliminar_post'),
    path('tipos_denuncias', TipoDenunciaListApi.as_view(), name='tipos_denuncias'),
    path('api/avisos', AvisoAPI.as_view(), name='avisos_api'),
    path('denuncia/<int:id_publicacion>/<int:id_tipo_denuncia>/', registrar_denuncia, name='denunciar'),
    path('ver/<int:post_id>', mostrar_post, name='ver_post'),
    path('avisos/marcar-revisado', marcar_avisos_revisados, name='marcar_avisos_revisados'),
]
