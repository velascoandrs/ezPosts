from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.posts.forms import *
from apps.posts.helpers import handle_uploaded_file
from apps.posts.models import *
from apps.usuarios.models import Afinidad
from django.views.generic import DetailView


def index_post(request):
    return HttpResponse("Index de los posts")


# Mostrar el contenido de un post v2
def mostrar_post(request, post_id):
    post = Post.objects.get(id=post_id)
    existe_denuncia = False
    if request.user.is_authenticated:
        if post.publicacion.denuncias.filter(usuario_denunciante=request.user.id):
            existe_denuncia = True
        if post.publicacion.autor.pk != request.user.id:
            Visualizacion.objects.create(post=post)
    return render(request, 'post/post_info.html', {'post': post, 'existe_denuncia': existe_denuncia})


# Mostrar el contenido de un post posts
class PostView(DetailView):
    model = Post
    template_name = 'post/post_info.html'
    context_object_name = "post"

    # Contar las visitas al post, se redefine el metodo get
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Solo cuenta visitas de usuarios registrados y que no sea el mismo autor
        if request.user.is_authenticated and self.object.autor.pk != request.user.id:
            Visualizacion.objects.create(post=self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
        post_publicacion = Publicacion.objects.create(
            autor=request.user
        )
        post_publicacion.save()
        post = Post.objects.create(
            titulo=titulo,
            portada=portada,
            afinidad=afinidad,
            contenido=contenido,
            publicacion=post_publicacion
        )
        post.save()
        return redirect('usuarios:ver_perfil', request.user.id)
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
        return redirect('usuarios:ver_perfil', request.user.id)
    # Renderizar el formulario en el template
    return render(request, 'post/actualizar_post.html', {'form': form})


# Vista para poder eliminar un Post
@login_required(login_url='/')
def eliminar_post(request, post_id):
    #  Encontrar el post
    post = get_object_or_404(Post, id=post_id)
    if post.publicacion.autor.id != request.user.id:
        return redirect('/')
    # Eliminar el post
    post.delete()
    return redirect('usuarios:ver_perfil', request.user.id)


# Vista encargada de registrar denuncias referentes a un post
@login_required(login_url="/")
def registrar_denuncia(request, id_publicacion, id_tipo_denuncia):
    # Se crea la denuncia respectiva
    denuncia = Denuncia.objects.create(
        tipo_decuncia_id=id_tipo_denuncia,
        usuario_denunciante_id=request.user.id
    )
    # Se encuentra el post que se denuncia
    publicacion = Publicacion.objects.get(pk=id_publicacion)
    tipo_denuncia = TipoDenuncia.objects.get(pk=id_tipo_denuncia)
    # Se crea el aviso para notificar al autor del post
    Aviso.objects.create(
        contenido=f"Tu publicacion ha sido denunciada por: {tipo_denuncia.nombre_tipo_denuncia}",
        publicacion=publicacion
    )
    publicacion.denuncias.add(denuncia)
    return JsonResponse({'respuesta': 'OK'})


#  Cambiar avisos por revisado
@login_required(login_url='/')
@csrf_exempt
def marcar_avisos_revisados(request):
    if request.method == 'POST':
        Aviso.objects \
            .filter(publicacion__autor__id=request.user.id) \
            .filter(esta_revisado=False) \
            .update(esta_revisado=True)
        return JsonResponse({'mensaje': 'OK'})
