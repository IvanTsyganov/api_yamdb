from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CategoryviewSet, GenreviewSet, TitleviewSet, UserViewSet, SignUpViewSet

from .views import (
    CategoryviewSet, GenreviewSet, TitleviewSet,
    ReviewViewSet, CommentViewSet,
                    )
router = routers.DefaultRouter()

router.register('categories', CategoryviewSet, basename='category')
router.register('genres', GenreviewSet, basename='genre')
router.register('titles', TitleviewSet, basename='title')
router.register(r'users', UserViewSet, basename='user')
router.register(r'signup', SignUpViewSet, basename='signup')


router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', include(router.urls)),
]
