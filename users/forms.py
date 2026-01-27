from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "phone_number", "country", "password1", "password2")


class ProfileForm(UserChangeForm):
    password = None  # скрываем поле пароля

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'avatar')
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone_number': 'Телефон',
            'country': 'Страна',
            'avatar': 'Аватар',
        }