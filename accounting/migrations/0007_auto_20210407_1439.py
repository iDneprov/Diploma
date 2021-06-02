# Generated by Django 3.1.7 on 2021-04-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='bank',
        ),
        migrations.AddField(
            model_name='account',
            name='bank',
            field=models.ManyToManyField(to='accounting.Bank'),
        ),
    ]
