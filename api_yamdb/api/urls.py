from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryviewSet, GenreviewSet, TitleviewSet,
    ReviewViewSet, CommentViewSet, UserViewSet, signup, TokenView
                    )
router = routers.DefaultRouter()

router.register('categories', CategoryviewSet, basename='category')
router.register('genres', GenreviewSet, basename='genre')
router.register('titles', TitleviewSet, basename='title')
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', TokenView, name='token'),

]
