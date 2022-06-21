from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .viewsets import PostViewSet

from .views import UserListGetUpdateView, UserLoginView, UserProfileView, UserRegistrationView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('list&update/', UserListGetUpdateView.as_view(), name="list&update"),
    path('', include(router.urls))
]