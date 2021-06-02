import django.db.models

from accounting.models import Bank, Contract, FinancialInstrument, Operation, Category, Stock
from yahoo_fin.stock_info import get_live_price as stockPrice

def getStockPrice(stock):
    if stock.currency == 'RUB':
        return stockPrice(stock.tiker + '.me')
    return stockPrice(stock.tiker)


def getCurrencyCoeff(fromCurrency, toCurrency):
    if fromCurrency != toCurrency:
        return stockPrice(f'{fromCurrency}{toCurrency}=X')
    else:
        return 1

def addBankAccount(request, bankName, FIName, FICurrency, FIBalance):
    try:
        bankObj = Bank.objects.get(name=bankName)
    except Bank.DoesNotExist:
        bankObj = Bank(name=bankName)
        bankObj.save()

    try:
        contractObj = Contract.objects.filter(userID=request.user).get(bankID=bankObj)
    except Contract.DoesNotExist:
        contractObj = Contract(bankID=bankObj, userID=request.user, name=f'Договор с банком {bankName}',
                               currency=FICurrency, type='B')
        contractObj.save()

    financialInstrumentObj = FinancialInstrument(contractID=contractObj, name=FIName, type='B',
                                                 currency=FICurrency, balance=FIBalance)
    financialInstrumentObj.save()


def addBrokerAccount(request, brokerName, accountName, accountCurrency, accountBalance):
    bankQuerySet = Bank.objects.filter(name=brokerName)
    if len(bankQuerySet) == 0:
        bankObj = Bank(name=brokerName)
        bankObj.save()
    else:
        bankObj = bankQuerySet[0]

    contractObj = Contract(bankID=bankObj, userID=request.user, name=accountName,
                           currency=accountCurrency, type='I')
    contractObj.save()

    financialInstrumentObj = FinancialInstrument(contractID=contractObj, name=accountCurrency, type='C',
                                                 currency=accountCurrency, balance=accountBalance)
    financialInstrumentObj.save()


def addOperation(request, FIObj, opCategory, opCurrency, opSum, type='S'):
    opSum = float(opSum)
    try:
        categoryObj = Category.objects.filter(name=opCategory).filter(type=type).get(userID=request.user)
    except Category.DoesNotExist:
        categoryObj = Category(name=opCategory, userID=request.user, type=type)
        categoryObj.save()

    operationObj = Operation(fromFinancialInstrumentID=FIObj, categoryID=categoryObj,
                             currency=opCurrency, sum=opSum, type=type)
    operationObj.save()
    coeff = 1 if type == 'S' else -1
    FIObj.balance -= coeff * opSum * getCurrencyCoeff(opCurrency, FIObj.currency)
    FIObj.save()


def addInvestOperation(contractName, currency, sum, type, tiker):
    contractObj = Contract.objects.filter(name=contractName)[0]
    allStocks = FinancialInstrument.objects.filter(contractID=contractObj)
    balance = allStocks.objects.filter(name=currency)
    if len(balance) == 0:
        balance = allStocks.objects.filter(name=contractObj.currency)
        sum *= getCurrencyCoeff(currency, balance.currency)
    else:
        balance = balance[0]

    if type == 'BS':
        balance.amount -= sum
        stockForSale = allStocks.objects.filter(stockID__tiker=tiker)
        #if
    elif type == 'SS':
        balance.amount += sum


def addTransfer(senderFIObj, receiverFIObj, transferSum):
    transferSum = float(transferSum)
    operationObj = Operation(type='T', sum=transferSum,
                             fromFinancialInstrumentID=senderFIObj, toFinancialInstrumentID=receiverFIObj,
                             currency=senderFIObj.currency)

    senderFIObj.balance -= transferSum
    receiverFIObj.balance += transferSum * getCurrencyCoeff(senderFIObj.currency, receiverFIObj.currency)
    senderFIObj.save()
    receiverFIObj.save()
    operationObj.save()


def getUserOperations(request):
    if request.user.is_authenticated:
        operations = Operation.objects.filter(fromFinancialInstrumentID__contractID__userID=request.user)
    else:
        operations = []
    return operations


def getBankAccounts(request):
    if request.user.is_authenticated:
        bankAccounts = FinancialInstrument.objects.filter(contractID__userID=request.user).filter(type='B')
    else:
        bankAccounts = []
    return bankAccounts


def bankAccountFormat(bankAccounts):
    colors = []
    CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
    for account in bankAccounts:
        if account.balance > 0:
            color = 'green'
        elif account.balance < 0:
            color = 'red'
        else:
            color = 'info'
        colors.append(color)
        account.balance = floatFormating(account.balance)
        account.currency = CURRENCY_TYPES[account.currency]
    return bankAccounts, colors


def getBrokerAccountBalance(account):
    balance = 0
    money = 0
    actives = FinancialInstrument.objects.filter(contractID=account)
    stocks = actives.filter(type='I')
    moneyAccounts = actives.filter(type='C')
    investedSum = 0
    for stock in stocks:
        currencyCoeff = getCurrencyCoeff(stock.stockID.currency, account.currency)
        balance += stock.amount * getStockPrice(stock.stockID) * currencyCoeff
        investedSum += stock.avgPrice * stock.amount * currencyCoeff
    sumDelta = balance - investedSum
    for moneyAccount in moneyAccounts:
        currencyCoeff = getCurrencyCoeff(moneyAccount.currency, account.currency)
        money += moneyAccount.balance * currencyCoeff
    balance += money
    percentageDifference = sumDelta / (investedSum + money) * 100
    isProfitable = True if sumDelta >= 0 else False
    return balance, sumDelta, percentageDifference, isProfitable

def getBrokerAccountBalanceStructureCurrency(account):
    currencys = set()
    balance = 0
    money = 0
    actives = FinancialInstrument.objects.filter(contractID=account)
    stocks = actives.filter(type='I')
    moneyAccounts = actives.filter(type='C')
    investedSum = 0
    for stock in stocks:
        currencyCoeff = getCurrencyCoeff(stock.stockID.currency, account.currency)
        balance += stock.amount * getStockPrice(stock.stockID) * currencyCoeff
        investedSum += stock.avgPrice * stock.amount * currencyCoeff
    sumDelta = balance - investedSum
    for moneyAccount in moneyAccounts:
        currencyCoeff = getCurrencyCoeff(moneyAccount.currency, account.currency)
        money += moneyAccount.balance * currencyCoeff
        currencys.add(moneyAccount.currency)
    balance += money
    percentageDifference = sumDelta / (investedSum + money) * 100
    return balance, stocks, moneyAccounts, currencys, sumDelta, percentageDifference


def getBrokerAccounts(request):
    if request.user.is_authenticated:
        brokerAccounts = Contract.objects.filter(userID=request.user).filter(type='I')
    else:
        brokerAccounts = []
    data = [getBrokerAccountBalance(account) for account in brokerAccounts]
    balance = []
    sumDelta = []
    percentageDifference = []
    isProfitable = []
    for d in data:
        balance.append(d[0])
        sumDelta.append(d[1])
        percentageDifference.append(d[2])
        isProfitable.append(d[3])
    return brokerAccounts, balance, sumDelta, percentageDifference#, isProfitable


def brokerAccountsFormat(brokerAccounts, balances, sumDelta, percentageDifference):
    CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
    balancesFormat = [floatFormating(balance) + ' ' + CURRENCY_TYPES[account.currency]
                      for account, balance in zip(brokerAccounts, balances)]
    sumDeltaFormat = [floatFormating(sd) + ' ' + CURRENCY_TYPES[account.currency]
                      for account, sd in zip(brokerAccounts, sumDelta)]
    percentageFormat = [floatFormating(i) for i in percentageDifference]
    return brokerAccounts, balancesFormat, sumDeltaFormat, percentageFormat


def getAccountStocks(brokerAccount):
    FinancialInstrument.objects.filter(contractID=brokerAccount)


def addCurrencyToBrokerAccount(account, currency):
    nuwCurr = FinancialInstrument(contractID=account, name=currency, currency=currency, type='C')
    nuwCurr.save()


def addStockOperation(account, buyTiker, buyQuantity, buyAvgPrice, buyCurrency, type='buy'):
    buyAvgPrice = float(buyAvgPrice)
    buyQuantity = float(buyQuantity)
    buyQuantity *= 1 if type == 'buy' else -1
    type = 'BS' if type == 'buy' else 'SS'

    try:
        stock = Stock.objects.get(tiker=buyTiker)
    except Stock.DoesNotExist:
        stock = Stock(tiker=buyTiker, currency=buyCurrency)
        stock.save()
    financialInstruments = FinancialInstrument.objects.filter(contractID=account)
    totalSumm = buyAvgPrice * buyQuantity

    try:
        stockFI = financialInstruments.get(stockID__tiker=buyTiker)
        total = stockFI.amount * stockFI.avgPrice + totalSumm
        stockFI.amount += buyQuantity
        stockFI.avgPrice = total / stockFI.amount
    except FinancialInstrument.DoesNotExist:
        stockFI = FinancialInstrument(contractID=account, stockID=stock, name=buyTiker, type='I', amount=buyQuantity,
                                      avgPrice=buyAvgPrice, currency=buyCurrency)
    stockFI.save()

    try:
        balance = financialInstruments.get(name=buyCurrency)
    except FinancialInstrument.DoesNotExist:
        balance = financialInstruments.get(name=account.currency)
        totalSumm *= getCurrencyCoeff(buyCurrency, balance.currency)
    balance.balance -= totalSumm
    balance.save()

    investOperation = Operation(fromFinancialInstrumentID=balance, toFinancialInstrumentID=stockFI, type=type, sum=-totalSumm, currency=balance.currency)
    investOperation.save()


def getBankAccountOperations(financialInstrument):
    operatonsFrom = Operation.objects.filter(fromFinancialInstrumentID=financialInstrument)
    operatonsTo = Operation.objects.filter(toFinancialInstrumentID=financialInstrument)
    operations = operatonsFrom | operatonsTo
    operations = operations.order_by('-dateTime')
    CURRENCY_TYPES = dict(financialInstrument.CURRENCY_TYPES)
    for operation in operations:
        operation.sum = floatFormating(operation.sum)
        operation.currency = CURRENCY_TYPES[operation.currency]
    return operations

def getAllSpending(request):
    if not request.user.is_authenticated:
        return []
    else:
        operations = Operation.objects.filter(fromFinancialInstrumentID__contractID__userID=request.user).filter(type='S')
        CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
        operations = operations.order_by('-dateTime')
        for operation in operations:
            operation.sum = floatFormating(operation.sum)
            operation.currency = CURRENCY_TYPES[operation.currency]
        return operations

def getAllIncomes(request):
    if not request.user.is_authenticated:
        return []
    else:
        operations = Operation.objects.filter(fromFinancialInstrumentID__contractID__userID=request.user).filter(type='I')
        CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
        operations = operations.order_by('-dateTime')
        for operation in operations:
            operation.sum = floatFormating(operation.sum)
            operation.currency = CURRENCY_TYPES[operation.currency]
        return operations

def getAccountsForTransfer(request):
    if not request.user.is_authenticated:
        return []
    else:
        accounts = FinancialInstrument.objects.filter(contractID__userID=request.user)
        bankAccounts = accounts.filter(type='B')
        brokerAccounts = accounts.filter(type='C')
        accounts = bankAccounts | brokerAccounts
        return accounts.order_by('type')

def getTotalBalance(request, bankAccounts, brokerAccounts, brokerBalances, currency='RUB'):
    if not request.user.is_authenticated:
        return
    else:
        balance = 0
        for account in bankAccounts:
            balance += account.balance * getCurrencyCoeff(account.currency, currency)
        for account, brokerBalance in zip(brokerAccounts, brokerBalances):
            balance += brokerBalance * getCurrencyCoeff(account.currency, currency)
        return balance


def totalBalanceFormat(balance, currency='RUB'):
    if balance > 0:
        color = 'green'
    elif balance < 0:
        color = 'red'
    else:
        color = 'info'
    CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
    return floatFormating(balance) + ' ' + CURRENCY_TYPES[currency], color


def getCurrencySymbols(QuerySet):
    currencySymbols = dict(FinancialInstrument.CURRENCY_TYPES)
    for object in QuerySet:
        object.currency = currencySymbols[object.currency]
    return QuerySet


def getContractStocksInfo(contract, stocks, moneyAccounts):
    pks = []
    names = []
    amounts = []
    currentValues = []
    priceDeltas = []
    earnings = []
    isProfitable = []
    CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
    for moneyAccount in moneyAccounts:
        pks.append(moneyAccount.pk)
        names.append(moneyAccount.name)
        amounts.append(floatFormating(moneyAccount.amount + moneyAccount.balance) + ' ' + CURRENCY_TYPES[moneyAccount.currency])
        currentValues.append(floatFormating((moneyAccount.amount + moneyAccount.balance) * getCurrencyCoeff(moneyAccount.currency, contract.currency)) + ' ' + CURRENCY_TYPES[contract.currency])
        if moneyAccount.amount == 0:
            priceDeltas.append('-')
            earnings.append('-')
            isProfitable.append('-')
        else:
            currentPrice = getStockPrice(moneyAccount.stockID.tiker)
            priceDelta = currentPrice - moneyAccount.avgPrice
            priceDeltas.append(floatFormating(abs(priceDelta) / moneyAccount.avgPrice * 100))
            earnings.append(floatFormating(moneyAccount.amount * abs(priceDelta)))
            isProfitable.append(True if priceDelta >= 0 else False)

    for stock in stocks:
        pks.append(stock.pk)
        names.append(stock.name)
        amounts.append(floatFormating(stock.amount))
        currentValues.append(floatFormating(stock.amount * getStockPrice(stock.stockID) * getCurrencyCoeff(stock.currency, contract.currency)) + ' ' + CURRENCY_TYPES[contract.currency])
        currentPrice = getStockPrice(stock.stockID)
        priceDelta = currentPrice - stock.avgPrice
        priceDeltas.append(floatFormating(abs(priceDelta) / stock.avgPrice * 100))
        earnings.append(floatFormating(stock.amount * abs(priceDelta) * getCurrencyCoeff(stock.currency, contract.currency)) + ' ' + CURRENCY_TYPES[contract.currency])
        isProfitable.append(True if priceDelta >= 0 else False)

    return zip(pks, names, amounts, currentValues, priceDeltas, isProfitable, earnings)


def floatFormating(a):
    sign = ''
    if a < 0:
        sign = '-'
        a *= -1
    if int(a) != a:
        a = format(a, '.2f')
        a = str(a)
        a1, a2 = a.split('.')
        l1 = len(a1)
        for i in range(l1 - 3, 0, -3):
            a11 = a1[:i]
            a12 = a1[i:]
            a1 = a11 + ' ' + a12
        return sign + a1 + '.' + a2
    else:
        a = format(a, '.0f')
        a1 = str(a)
        l1 = len(a1)
        for i in range(l1 - 3, 0, -3):
            a11 = a1[:i]
            a12 = a1[i:]
            a1 = a11 + ' ' + a12
        return sign + a1

def accBallanceList(accounts):
    CURRENCY_TYPES = dict(FinancialInstrument.CURRENCY_TYPES)
    for account in accounts:
        account.balance = floatFormating(account.balance) + ' ' + CURRENCY_TYPES[account.currency]
    return accounts


