from django.urls import path
from apps.posts.views import *

urlpatterns = [
    path('index', index_post,name='index_post'),
    path('crearPost', crear_post, name='crear_post'),
    #path('ver/<pk>', PostView.as_view(),name='ver_post'),
    path('api/post', PostDetalleListApi.as_view(), name='post_list'),
    path('actualizar/<int:post_id>/', editar_post, name='editar_post'),
    path('eliminar/<int:post_id>/', eliminar_post, name='eliminar_post'),
    path('tipos_denuncias', TipoDenunciaListApi.as_view(), name='tipos_denuncias'),
    path('denuncia/<int:id_post>/<int:id_tipo_denuncia>/', registrar_denuncia, name='denunciar'),
    path('ver/<int:post_id>', mostrar_post, name='ver_post'),
]
