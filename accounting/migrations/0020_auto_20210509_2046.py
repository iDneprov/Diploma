# Generated by Django 3.1.7 on 2021-05-09 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0019_auto_20210506_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='financialinstrument',
            name='currency',
            field=models.CharField(choices=[('RUB', '₽'), ('USD', '$'), ('EUR', '€'), ('GBP', '£'), ('JPY', '¥'), ('CHF', '₣'), ('CNY', '¥')], default='RUB', max_length=3, verbose_name='Базовая валюта'),
        ),
    ]
