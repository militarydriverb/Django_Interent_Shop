from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone", blank=True, null=True, help_text="Enter Phone number")
    country = models.CharField(max_length=50, blank=True, null=True)
    token = models.CharField(max_length=64, blank=True, null=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Проверяем, пустое ли имя (удаляем пробелы для надежности)
        if not self.first_name or self.first_name.strip() == "":
            if self.email and '@' in self.email:
                # 1. Берем часть до собаки
                name_part = self.email.split('@')[0]
                # 2. Делаем первую букву заглавной и сохраняем
                self.first_name = name_part.capitalize()  # или .title()

        super().save(*args, **kwargs)
