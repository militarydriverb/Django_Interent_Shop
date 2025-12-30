from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to="blog/previews", verbose_name="Превью", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Сохраняем объект
        super().save(*args, **kwargs)
        
        # Проверяем, достиг ли счетчик просмотров 10
        if self.views_count == 10:
            send_mail(
                subject='Поздравляем с достижением!',
                message=f'Ваша статья "{self.title}" достигла 10 просмотров! Поздравляем!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
