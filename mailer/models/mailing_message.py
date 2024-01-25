from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.const import NULLABLE


class MailingMessage(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Сообщение')
    author = models.ForeignKey(
        to=get_user_model(),
        **NULLABLE,
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mailer:message_detail', kwargs={'pk': self.pk})
