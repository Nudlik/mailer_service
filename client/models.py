from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.const import NULLABLE


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='Почтовый ящик')
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=100, **NULLABLE, verbose_name='Заметка')
    owner = models.ForeignKey(
        to=get_user_model(),
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name='client',
        verbose_name='Владелец',
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']
        permissions = [
            ('view_client_list', 'Может просматривать список клиентов')
        ]

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('client:client_detail', kwargs={'pk': self.pk})
