from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

User = get_user_model


class User(AbstractUser):
    """Кастомная модель User."""

    email = models.EmailField(verbose_name='Email',
                              help_text='Введите свою почту',
                              max_length=254,
                              unique=True,
                              )
    first_name = models.CharField(verbose_name='Имя',
                                  help_text='Введите свое имя',
                                  max_length=150,
                                  )
    last_name = models.CharField(verbose_name='Фамилия',
                                 help_text='Введите свою фамилию',
                                 max_length=150,
                                 )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriber',
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscribing')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe',
            )
        ]
        ordering = ['id']
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
