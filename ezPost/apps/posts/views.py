from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework import generics
from apps.posts.forms import *
from apps.posts.helpers import handle_uploaded_file
from apps.posts.models import Visualizacion
from apps.usuarios.models import Afinidad
from django.views.generic import ListView, DetailView
from apps.posts.serializers import PostDetalleSerializado


def index_post(request):
    return HttpResponse("Index de los posts")


# Mostrar 10 ultimos posts clase prototipo
class PostView(DetailView):
    model = Post
    template_name = 'post/post_info.html'
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated and self.object.autor.pk != request.user.id:
            Visualizacion.objects.create(post=self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostDetalleListApi(generics.ListAPIView):
    serializer_class = PostDetalleSerializado
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-pk')
        titulo = self.request.query_params.get('titulo', None)
        if titulo is not None:
            queryset = queryset.filter(titulo__contains=titulo)
        return queryset


# Vista que permitira la creacion del post
@login_required(login_url='/')
def crear_post(request):
    if request.method == 'POST':

            titulo = request.POST.get('titulo', '')
            portada = request.FILES['portada']
            handle_uploaded_file(portada)
            contenido = request.POST.get('contenido', '')
            afinidad_pk = request.POST.get('afinidad', '')
            afinidad = Afinidad.objects.get(pk=afinidad_pk)
            post = Post.objects.create(
                        autor=request.user,
                        titulo=titulo,
                        portada=portada,
                        afinidad=afinidad,
                        contenido=contenido
            )
            post.save()
            return redirect('usuarios:mostrar_info')
    else:
        form = PostFormulario()
    return render(request, 'post/crear_post.html', {'form': form})

#  https://docs.djangoproject.com/es/2.1/topics/http/file-uploads/

