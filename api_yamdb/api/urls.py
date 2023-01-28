from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryviewSet, GenreviewSet, TitleviewSet,
    ReviewViewSet, CommentViewSet, UserViewSet, signup, TokenView

from rest_framework.authtoken import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    ReviewViewSet, CommentViewSet, UserViewSet, SignUpViewSet
                    )
router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', TokenView, name='token'),


    path('v1/', include(router.urls)),
    path('v1/auth/token/', views.obtain_auth_token),
    path('api/v1/auth/signup/`', views.obtain_auth_token),
    path('v1/auth/signup/', include(router.urls)),
]
