# Generated by Django 3.1.7 on 2021-05-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0027_auto_20210515_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinstrument',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='financialinstrument',
            name='avgPrice',
            field=models.FloatField(default=0, verbose_name='Текущая цена'),
        ),
    ]
