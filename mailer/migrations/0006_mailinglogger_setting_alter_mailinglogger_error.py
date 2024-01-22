# Generated by Django 4.2.7 on 2024-01-22 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0005_mailingmessage_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglogger',
            name='setting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log', to='mailer.mailingsettings', verbose_name='Рассылка'),
        ),
        migrations.AlterField(
            model_name='mailinglogger',
            name='error',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера'),
        ),
    ]