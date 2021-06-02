from django.contrib import admin
from accounting.models import Bank, Contract, Stock, FinancialInstrument, Operation, Category

admin.site.register(Bank)
admin.site.register(Contract)
admin.site.register(Stock)
admin.site.register(FinancialInstrument)
admin.site.register(Operation)
admin.site.register(Category)
