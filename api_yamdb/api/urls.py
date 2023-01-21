from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import (
    CategoryviewSet, GenreviewSet, TitleviewSet,
    ReviewViewSet, CommentViewSet,
                    )
router = routers.DefaultRouter()

router.register('categories', CategoryviewSet, basename='category')
router.register('genres', GenreviewSet, basename='genre')
router.register('titles', TitleviewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.obtain_auth_token),
    path('/api/v1/auth/signup/`', views.obtain_auth_token),
]
