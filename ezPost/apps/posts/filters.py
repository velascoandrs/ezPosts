from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from apps.posts.models import Post

class PostFilter(FilterSet):
    afinidad = CharFilter(method='filtro_afinidad',)
    titulo = CharFilter(method='filtro_titulo')
    autor = NumberFilter(field_name='autor')

    class Meta:
        model = Post
        fields = {
            'afinidad',
            'titulo',
            'autor',
        }

    def filtro_afinidad(self, queryset, name,value):
        values = value.split(',')
        return queryset.filter(afinidad__in=values)

    def filtro_titulo(self, queryset, name,value):
        return queryset.filter(titulo__contains=value)


