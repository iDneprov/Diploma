# Generated by Django 3.1.7 on 2021-05-09 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0020_auto_20210509_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
