# Generated by Django 4.2.7 on 2024-01-17 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0003_alter_client_comment_alter_client_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingLogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')),
                ('status', models.CharField(choices=[('success', 'успешно'), ('error', 'ошибка')], max_length=7, verbose_name='Статус попытки')),
                ('error', models.CharField(max_length=255, verbose_name='Ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Тема письма')),
                ('message', models.TextField(verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateField(verbose_name='Время начала')),
                ('time_end', models.DateField(verbose_name='Время конца')),
                ('frequency', models.CharField(choices=[('daily', 'ежедневно'), ('weekly', 'еженедельно'), ('monthly', 'ежемесячно')], max_length=7, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('draft', 'черновик'), ('created', 'создана'), ('active', 'активна'), ('inactive', 'неактивна')], max_length=8, verbose_name='Статус')),
                ('clients', models.ManyToManyField(to='client.client', verbose_name='Клиенты')),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setting', to='mailer.mailingmessage', verbose_name='Письмо')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setting', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]
