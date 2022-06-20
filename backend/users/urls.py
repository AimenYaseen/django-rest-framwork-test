from django.urls import path

from .views import UserChangePasswordView, UserListGetUpdateView, UserLoginView, UserProfileView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('changepassword/', UserChangePasswordView.as_view(), name="changepassword"),
    path('list&update/', UserListGetUpdateView.as_view(), name="list&update")
]