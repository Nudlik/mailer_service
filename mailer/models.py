from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from client.models import Client

NULLABLE = {
    'blank': True,
    'null': True,
}


class MailingSettings(models.Model):

    class FREQUENCY(models.TextChoices):
        DAILY = 'daily', 'ежедневно'
        WEEKLY = 'weekly', 'еженедельно'
        MONTHLY = 'monthly', 'ежемесячно'

    class STATUS(models.TextChoices):
        DRAFT = 'draft', 'черновик'
        CREATED = 'created', 'создана'
        ACTIVE = 'active', 'активна'
        INACTIVE = 'inactive', 'неактивна'

    title = models.CharField(max_length=100, verbose_name='Название рассылки')
    time_start = models.DateField(verbose_name='Время начала')
    time_end = models.DateField(verbose_name='Время конца')
    frequency = models.CharField(choices=FREQUENCY.choices, max_length=7, verbose_name='Периодичность')
    status = models.CharField(choices=STATUS.choices, max_length=8, verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    mail = models.ForeignKey(
        to='MailingMessage',
        on_delete=models.CASCADE,
        related_name='setting',
        verbose_name='Письмо',
    )
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name='setting',
        verbose_name='Владелец',
    )
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_view_all_fields', 'Может просматривать всю админку'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mailer:settings_detail', kwargs={'pk': self.pk})

    @property
    def get_status(self):
        return dict(self.STATUS.choices).get(self.status)

    @property
    def get_frequency(self):
        return dict(self.FREQUENCY.choices).get(self.frequency)


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
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mailer:message_detail', kwargs={'pk': self.pk})


class MailingLogger(models.Model):

    class STATUS(models.TextChoices):
        SUCCESS = 'success', 'успешно'
        ERROR = 'error', 'ошибка'

    date = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=7, choices=STATUS.choices, verbose_name='Статус попытки')
    error = models.CharField(max_length=255, verbose_name='Ответ почтового сервера')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return f'{self.date} {self.status}'
