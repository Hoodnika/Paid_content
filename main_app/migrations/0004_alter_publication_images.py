# Generated by Django 5.0.6 on 2024-08-04 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_subscription_active_until_subscription_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, to='main_app.image', verbose_name='изображения'),
        ),
    ]
