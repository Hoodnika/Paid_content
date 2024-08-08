from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import AUTH_USER_MODEL
from config.special_elements import NULLABLE


class Subscription(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='subscription')
    is_active = models.BooleanField(default=False, verbose_name='Активна ли подписка')
    update_at = models.DateTimeField(verbose_name='День обновления подписки', **NULLABLE)
    end_at = models.DateTimeField(verbose_name='Подписка активна до', **NULLABLE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Publication(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец пубилкации',
                              related_name='publication')
    title = models.CharField(max_length=300, verbose_name='название публикации')
    preview = models.ImageField(upload_to='publication/preview', verbose_name='превью', **NULLABLE)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True, **NULLABLE)
    slug = models.CharField(max_length=150, verbose_name='Ссылка', unique=True)
    description = models.TextField(verbose_name='Краткое описание публикации')
    content = CKEditor5Field(verbose_name='содержание публикации', config_name='extends')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
