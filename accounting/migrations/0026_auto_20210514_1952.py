# Generated by Django 3.1.7 on 2021-05-14 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0025_remove_financialinstrument_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='currentPrice',
            field=models.FloatField(null=True, verbose_name='текущая цена'),
        ),
    ]
