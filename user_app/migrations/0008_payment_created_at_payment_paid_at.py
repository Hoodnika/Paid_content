# Generated by Django 5.0.6 on 2024-08-07 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_payment_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 7, 15, 58, 19, 262411, tzinfo=datetime.timezone.utc), verbose_name='Дата создания платежа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 7, 15, 58, 29, 676363, tzinfo=datetime.timezone.utc), verbose_name='Дата оплаты платежа'),
            preserve_default=False,
        ),
    ]
