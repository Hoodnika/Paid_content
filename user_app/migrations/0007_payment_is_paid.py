# Generated by Django 5.0.6 on 2024-08-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_remove_payment_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Статус прохождения платежа'),
        ),
    ]
