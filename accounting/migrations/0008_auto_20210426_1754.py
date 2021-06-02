# Generated by Django 3.1.7 on 2021-04-26 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0007_auto_20210407_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('type', models.CharField(max_length=50, verbose_name='Тип финансового инструмента')),
                ('picture', models.IntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Категория транзакции',
                'verbose_name_plural': 'Категории транзакции',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('currency', models.CharField(max_length=3, verbose_name='Базовая валюта')),
                ('type', models.CharField(choices=[('B', 'Банковский'), ('I', 'Инвестиционный')], max_length=1, verbose_name='Тип договора')),
                ('picture', models.ImageField(upload_to='ContractsPictures')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договоры',
            },
        ),
        migrations.CreateModel(
            name='FinancialInstrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('type', models.CharField(choices=[('B', 'Банковский'), ('I', 'Инвестиционный')], max_length=1, verbose_name='Тип финансового инструмента')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('avgPrice', models.FloatField(verbose_name='Текущая цена')),
                ('currency', models.CharField(max_length=5, verbose_name='Валюта')),
                ('interest', models.FloatField(verbose_name='текущая цена')),
                ('contractID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.contract')),
            ],
            options={
                'verbose_name': 'Финансовый инструмент',
                'verbose_name_plural': 'Финансовые инструменты',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Action', 'Акция'), ('Bond', 'Облигация'), ('ETF', 'ETF'), ('Currency', 'Валюта'), ('Other', 'Другое')], max_length=8, verbose_name='Тип ценной бумаги')),
                ('tiker', models.CharField(max_length=10, verbose_name='Тикер')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('currentPrice', models.FloatField(verbose_name='текущая цена')),
            ],
            options={
                'verbose_name': 'Ценная бумага',
                'verbose_name_plural': 'Ценные бумаги',
            },
        ),
        migrations.RenameField(
            model_name='bank',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='bank',
            name='picture',
            field=models.ImageField(default='BanksPictures/default.jpg', upload_to='BanksPictures'),
        ),
        migrations.AddField(
            model_name='bank',
            name='type',
            field=models.CharField(choices=[('B', 'Банк'), ('I', 'Броккер')], max_length=2, null=True, verbose_name='Тип банка'),
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('BG', 'Buying goods'), ('INC', 'Income'), ('TRANS', 'Transfer'), ('BS', 'Buying a stock'), ('SS', 'Sale of stock'), ('DIV', 'Dividends')], max_length=5, verbose_name='Тип финансового инструмента')),
                ('summ', models.FloatField(verbose_name='Сумма сделки')),
                ('dateTime', models.DateTimeField(verbose_name='Дата и время совершения сделки')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('categoryID', models.ManyToManyField(to='accounting.Category')),
                ('fromFinancialInstrumentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromFinancialInstrument', to='accounting.financialinstrument')),
                ('parentOperationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.operation')),
                ('toFinancialInstrumentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toFinancialInstrument', to='accounting.financialinstrument')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
            },
        ),
        migrations.AddField(
            model_name='financialinstrument',
            name='stockID',
            field=models.ManyToManyField(to='accounting.Stock'),
        ),
        migrations.AddField(
            model_name='contract',
            name='bankID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.bank'),
        ),
        migrations.AddField(
            model_name='contract',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]