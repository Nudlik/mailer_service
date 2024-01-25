from django.db import models

from utils.const import NULLABLE


class MailingLogger(models.Model):
    class STATUS(models.TextChoices):
        SUCCESS = 'success', 'успешно'
        ERROR = 'error', 'ошибка'

    date = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=7, choices=STATUS.choices, verbose_name='Статус попытки')
    error = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')
    setting = models.ForeignKey(
        to='MailingSettings',
        **NULLABLE,
        on_delete=models.SET_NULL,
        verbose_name='Рассылка',
        related_name='log',
    )

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return f'{self.date} {self.status}'
