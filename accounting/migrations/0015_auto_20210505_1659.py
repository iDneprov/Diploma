# Generated by Django 3.1.7 on 2021-05-05 16:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_financialinstrument_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='type',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='price',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='summ',
        ),
        migrations.AddField(
            model_name='operation',
            name='sum',
            field=models.FloatField(default=0, verbose_name='Сумма сделки'),
        ),
        migrations.RemoveField(
            model_name='operation',
            name='categoryID',
        ),
        migrations.AddField(
            model_name='operation',
            name='categoryID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toCategory', to='accounting.category'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='dateTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время совершения сделки'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='type',
            field=models.CharField(choices=[('BG', 'Buying goods'), ('INC', 'Income'), ('TRANS', 'Transfer'), ('BS', 'Buying a stock'), ('SS', 'Sale of stock'), ('DIV', 'Dividends')], max_length=5, verbose_name='Тип операции'),
        ),
    ]
