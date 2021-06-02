from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Bank(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    image = models.ImageField(upload_to='BanksPictures', default='BanksPictures/default.png')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'


class Contract(models.Model):
    CONTRACT_TYPES = (
        ('B', 'Банковский'),
        ('I', 'Инвестиционный')
    )
    CURRENCY_TYPES = (
        ('RUB', 'Российский рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('GBP', 'Фунт стерлингов Великобритании'),
        ('JPY', 'Японская йена'),
        ('CHF', 'Швейцарский франк'),
        ('CNY', 'Китайский юань'),
    )
    bankID = models.ForeignKey(Bank, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=50)
    currency = models.CharField('Базовая валюта', max_length=3, choices=CURRENCY_TYPES, default='RUB')
    type = models.CharField('Тип договора', max_length=1, choices=CONTRACT_TYPES)

    def __str__(self):
        return f'{self.name} : {self.type}'

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'


class Stock(models.Model):
    STOCK_TYPES = (
        ('Action', 'Акция'),
        ('Bond', 'Облигация'),
        ('ETF', 'ETF'),
        ('Currency', 'Валюта'),
        ('Other', 'Другое')
    )
    CURRENCY_TYPES = (
        ('RUB', 'Российский рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('GBP', 'Фунт стерлингов Великобритании'),
        ('JPY', 'Японская йена'),
        ('CHF', 'Швейцарский франк'),
        ('CNY', 'Китайский юань'),
    )
    #type = models.CharField('Тип ценной бумаги', max_length=8, choices=STOCK_TYPES)
    tiker = models.CharField('Тикер', max_length=10)
    currency = models.CharField('Базовая валюта', max_length=3, choices=CURRENCY_TYPES, default='RUB')
    currentPrice = models.FloatField('текущая цена', null=True)

    def __str__(self):
        return f'{self.tikerCode} : {self.currentPrice}'

    class Meta:
        verbose_name = 'Ценная бумага'
        verbose_name_plural = 'Ценные бумаги'


class FinancialInstrument(models.Model):
    FINANCIAL_INSTRUMENT_TYPES = (
        ('B', 'Банковский'),
        ('I', 'Инвестиционный'),
        ('C', 'Валюта')
    )
    CURRENCY_TYPES = (
        ('RUB', '₽'),
        ('USD', '$'),
        ('EUR', '€'),
        ('GBP', '£'),
        ('JPY', '¥'),
        ('CHF', '₣'),
        ('CNY', '¥'),
    )

    contractID = models.ForeignKey(Contract, on_delete=models.CASCADE)
    stockID = models.ForeignKey(Stock, null=True, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=50)
    type = models.CharField('Тип финансового инструмента', max_length=1, choices=FINANCIAL_INSTRUMENT_TYPES)
    balance = models.FloatField('Баланс счёта', default=0)
    amount = models.FloatField('Количество', default=0)
    avgPrice = models.FloatField('Текущая цена', default=0)
    currency = models.CharField('Базовая валюта', max_length=3, choices=CURRENCY_TYPES, default='RUB')

    def __str__(self):
        return f'{self.name} : {self.type}'

    class Meta:
        verbose_name = 'Финансовый инструмент'
        verbose_name_plural = 'Финансовые инструменты'


class Category(models.Model):
    CATEGORY_TYPES = (
        ('S', 'Расходы'),
        ('I', 'Доходы'),
        ('T', 'Переводы')
    )

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=50)
    type = models.CharField('Тип категории', max_length=1, choices=CATEGORY_TYPES, default='S')

    def __str__(self):
        return f'{self.name} : {self.type}'

    class Meta:
        verbose_name = 'Категория транзакции'
        verbose_name_plural = 'Категории транзакции'


class Operation(models.Model):
    OPERATION_TYPES = (
        ('S', 'Spending'),
        ('I', 'Income'),
        ('T', 'Transfer'),
        ('BS', 'Buying a stock'),
        ('SS', 'Sale of stock'),
        ('DIV', 'Dividends')
    )
    CURRENCY_TYPES = (
        ('RUB', 'Российский рубль'),
        ('USD', 'Доллар США'),
        ('EUR', 'Евро'),
        ('GBP', 'Фунт стерлингов Великобритании'),
        ('JPY', 'Японская йена'),
        ('CHF', 'Швейцарский франк'),
        ('CNY', 'Китайский юань'),
    )

    #parentOperationID = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    fromFinancialInstrumentID = models.ForeignKey(FinancialInstrument, related_name='fromFinancialInstrument', on_delete=models.CASCADE)
    toFinancialInstrumentID = models.ForeignKey(FinancialInstrument, related_name='toFinancialInstrument', on_delete=models.CASCADE, null=True)
    categoryID = models.ForeignKey(Category, related_name='toCategory', on_delete=models.CASCADE, null=True)
    type = models.CharField('Тип операции', max_length=5, choices=OPERATION_TYPES)
    sum = models.FloatField('Сумма сделки', default=0)
    dateTime = models.DateTimeField('Дата и время совершения сделки', default=now)
    currency = models.CharField('Базовая валюта', max_length=3, choices=CURRENCY_TYPES, default='RUB')

    def __str__(self):
        return f'{self.type} : {self.sum} : {self.currency}'

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
