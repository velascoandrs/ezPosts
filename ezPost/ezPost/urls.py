"""ezPost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from ckeditor_uploader import views as uploader_views


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('usuario/', include(('apps.usuarios.urls','usuarios'), namespace="usuarios")),
    path('post/', include(('apps.posts.urls','posts'), namespace="posts")),
    path('', include('django.contrib.auth.urls')),
    # REDES SOCIALES
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^ckeditor/upload/',uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/',never_cache(uploader_views.browse), name='ckeditor_browse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

