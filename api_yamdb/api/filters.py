from django_filters import rest_framework as title_filters

from reviews.models import Title


class Titlefilter(title_filters.FilterSet):
    name = title_filters.CharFilter(field_name = 'name')
    year = title_filters.NumberFilter