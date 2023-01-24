from django_filters import rest_framework as title_filters

from reviews.models import Title


class TitlesFilter(title_filters.FilterSet):
    name = title_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = title_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = title_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['name', 'genre', 'category', 'year']