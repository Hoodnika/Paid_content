# Generated by Django 5.0.6 on 2024-08-07 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_rename_active_until_subscription_end_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]
