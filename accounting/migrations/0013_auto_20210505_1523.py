# Generated by Django 3.1.7 on 2021-05-05 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_auto_20210505_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinstrument',
            name='stockID',
            field=models.ManyToManyField(to='accounting.Stock'),
        ),
    ]
