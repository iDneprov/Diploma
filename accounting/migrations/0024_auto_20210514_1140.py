# Generated by Django 3.1.7 on 2021-05-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0023_auto_20210511_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinstrument',
            name='stockID',
            field=models.ManyToManyField(null=True, to='accounting.Stock'),
        ),
        migrations.AlterField(
            model_name='financialinstrument',
            name='type',
            field=models.CharField(choices=[('B', 'Банковский'), ('I', 'Инвестиционный'), ('C', 'Валюта')], max_length=1, verbose_name='Тип финансового инструмента'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='type',
            field=models.CharField(choices=[('S', 'Spending'), ('I', 'Income'), ('T', 'Transfer'), ('BS', 'Buying a stock'), ('SS', 'Sale of stock'), ('DIV', 'Dividends')], max_length=5, verbose_name='Тип операции'),
        ),
    ]
