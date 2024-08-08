from django.contrib.auth.models import AbstractUser
from django.db import models

from config.special_elements import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почтовый адрес')
    open_email = models.BooleanField(default=True,
                                     verbose_name='Могут ли с вами связаться по почтовому адресу')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефона',
                                    help_text='Обязательное поле')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    token_verification = models.CharField(max_length=50, verbose_name='код верификации', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания профиля', auto_now_add=True)
    about = models.TextField(verbose_name='О себе', **NULLABLE)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = []


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', related_name='payment',
                              **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='сумма оплаты')
    session_id = models.CharField(max_length=300, verbose_name=' id сессии')
    is_paid = models.BooleanField(default=False, verbose_name='Статус прохождения платежа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания платежа')
    paid_at = models.DateTimeField(verbose_name='Дата оплаты платежа', **NULLABLE)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
