# Generated by Django 3.1.7 on 2021-05-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20210504_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='currency',
            field=models.CharField(choices=[('RUB', 'Российский рубль'), ('USD', 'Доллар США'), ('EUR', 'Евро'), ('GBP', 'Фунт стерлингов Великобритании'), ('JPY', 'Японская йена'), ('CHF', 'Швейцарский франк'), ('CNY', 'Китайский юань')], max_length=3, verbose_name='Базовая валюта'),
        ),
    ]
