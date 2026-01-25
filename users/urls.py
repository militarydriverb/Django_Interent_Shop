from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import UserCreateView, ProfileUpdateView, ProfileDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(template_name='register.html'), name='registration'),
    path('profile/', ProfileDetailView.as_view(template_name='profile.html'), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(template_name='profile_edit.html'), name='profile_edit'),
]