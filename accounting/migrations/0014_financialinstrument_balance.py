# Generated by Django 3.1.7 on 2021-05-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_auto_20210505_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialinstrument',
            name='balance',
            field=models.FloatField(default=0, verbose_name='Баланс счёта'),
        ),
    ]
