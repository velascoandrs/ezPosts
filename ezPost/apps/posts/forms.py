from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms.models import ModelForm
from apps.posts.models import Post


class PostFormulario(ModelForm):
    contenido = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['titulo', 'afinidad', 'portada', 'contenido']