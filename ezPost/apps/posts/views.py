from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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


# Vista para poder actualizar el contenido de un Post
@login_required(login_url='/')
def editar_post(request, post_id):
    #  Encontrar el post
    post = get_object_or_404(Post, id=post_id)
    # Validar que el usuario es propietario del post
    if post.autor.id != request.user.id:
        # Si no es propietario sera sera redireccionado al inicio
        return redirect('/')
    # Crear un formulario y llenarno con la instancia del post encontrado
    form = PostFormulario(request.POST or None, instance=post)
    # Verificar que el formulario este llenado correctamente
    if form.is_valid():
        # Guardar los cambios
        form.save()
        # Redireccionar a la pagina de informacion del perfil del usuario
        return redirect('usuarios:mostrar_info')
    # Renderizar el formulario en el template
    return render(request, 'post/actualizar_post.html', {'form': form})


# Vista para poder eliminar un Post
@login_required(login_url='/')
def eliminar_post(request, post_id):
    #  Encontrar el post
    post = get_object_or_404(Post, id=post_id)
    if post.autor.id != request.user.id:
        return redirect('/')
    # Eliminar el post
    post.delete()
    return redirect('usuarios:mostrar_info')
#  https://docs.djangoproject.com/es/2.1/topics/http/file-uploads/

