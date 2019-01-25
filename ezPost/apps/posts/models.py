from django.db import models
from apps.usuarios.models import User, Afinidad
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.from ckeditor.fields import RichTextField


class TipoValoracion(models.Model):
    nombre_tipo_valoracion = models.CharField(max_length=30, blank=False, null=False)


class Valoracion(models.Model):
    tipo_valoracion = models.ForeignKey(TipoValoracion, blank=False, on_delete=models.CASCADE, null=False)
    usuario_valorador = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=False)
    fecha_valoracion = models.DateField(null=False, blank=False, auto_now=True)


class TipoDenuncia(models.Model):
    nombre_tipo_denuncia = models.CharField(max_length=30, blank=False, null=False)


class Denuncia(models.Model):
    tipo_decuncia = models.ForeignKey(TipoDenuncia, blank=False, on_delete=models.CASCADE, null=False)
    fecha_denuncia = models.DateField(null=False, blank=False, auto_now=True)
    usuario_denunciante = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=False)


class Post(models.Model):
    titulo = models.CharField(max_length=30, blank=False, null=False)
    portada = models.ImageField(default='ninguna', upload_to='post/portadas', blank=False, null=False)
    autor = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=False)
    afinidad = models.ForeignKey(Afinidad, null=False, blank=False, on_delete=models.CASCADE)
    contenido = RichTextUploadingField(null=False, blank=False)
    fecha_creacion = models.DateField(null=False, blank=False, auto_now=True)
    denuncias = models.ManyToManyField(Denuncia, blank=True, related_name='denuncias')
    valoraciones = models.ManyToManyField(Valoracion, blank=True, related_name='valoraciones')


class Visualizacion(models.Model):
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)


