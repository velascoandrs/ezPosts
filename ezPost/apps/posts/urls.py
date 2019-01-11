from django.urls import  path
from apps.posts.views import *

urlpatterns = [
    path('index',index_post,name='index_post'),
    path('crearPost', crear_post, name='crear_post'),
    path('api/post', PostDetalleListApi.as_view(), name='post_list')
]
