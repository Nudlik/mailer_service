# Generated by Django 4.2.7 on 2024-01-25 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_client_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['id'], 'permissions': [('view_client_list', 'Может просматривать список клиентов')], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
    ]
