from django.urls import path, include
from rest_framework import routers

from api.v1.views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, UserViewSet, signup, obtain_token,
    ReviewViewSet, CommentViewSet
)


router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register('users', UserViewSet, basename='user')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', obtain_token, name='token'),
]
