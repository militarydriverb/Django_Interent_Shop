from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone", blank=True, null=True, help_text="Enter Phone number")
    country = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email.split('@')[0].title()