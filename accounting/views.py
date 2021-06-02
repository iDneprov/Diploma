from django.shortcuts import render, redirect, get_object_or_404
from accounting.operations import addBankAccount, addOperation, addTransfer, getUserOperations, getBankAccounts, \
    floatFormating, getBankAccountOperations, getCurrencySymbols, getAccountsForTransfer, accBallanceList, \
    getAllSpending, getAllIncomes, addBrokerAccount, getBrokerAccounts, bankAccountFormat, brokerAccountsFormat, \
    getBrokerAccountBalanceStructureCurrency, addCurrencyToBrokerAccount, addStockOperation, getContractStocksInfo, \
    getTotalBalance, totalBalanceFormat
from accounting.models import FinancialInstrument, Category, Operation, Contract, Bank

def bankAccountView(request, pk):
    if request.user.is_anonymous:
        return redirect('login')
    bankAccount = get_object_or_404(FinancialInstrument.objects.filter(contractID__userID=request.user), pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        if 'opSum' in request.POST:
            opCurrency = request.POST['opCurrency']
            opCategory = request.POST['opCategory']
            opSum = request.POST['opSum']
            addOperation(request, bankAccount, opCategory, opCurrency, opSum, type='S')

        if 'incSum' in request.POST:
            opCurrency = request.POST['incCurrency']
            opCategory = request.POST['incCategory']
            opSum = request.POST['incSum']
            addOperation(request, bankAccount, opCategory, opCurrency, opSum, type='I')

        if 'transSum' in request.POST:
            transSum = request.POST['transSum']
            toAcc = request.POST['toAcc']
            addTransfer(bankAccount, FinancialInstrument.objects.get(pk=toAcc), transSum)
    balance = floatFormating(bankAccount.balance)

    categories = Category.objects.filter(userID=request.user)
    spendingsCategories = categories.filter(type='S')
    incomeCategories = categories.filter(type='I')
    operations = getBankAccountOperations(bankAccount)
    symbol = dict(FinancialInstrument.CURRENCY_TYPES)[bankAccount.currency]
    CURRENCY_TYPES = FinancialInstrument.CURRENCY_TYPES
    #operations = getCurrencySymbols(operations)
    accounts = getAccountsForTransfer(request)
    context = {'bankAccount': bankAccount, 'balance': balance, 'CURRENCY_TYPES': CURRENCY_TYPES,
               'spendingsCategories': spendingsCategories, 'incomeCategories': incomeCategories,
               'operations': operations, 'symbol': symbol, 'accounts': accounts, 'operationsLen': len(operations)}
    return render(request, 'accounting/BankAccount.html', context=context)

def brokerAccountView(request, pk):
    if request.user.is_anonymous:
        return redirect('login')
    account = get_object_or_404(Contract.objects.filter(userID=request.user), pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        if 'buyTiker' in request.POST:
            buyTiker = request.POST['buyTiker']
            buyQuantity = request.POST['buyQuantity']
            buyAvgPrice = request.POST['buyAvgPrice']
            buyCurrency = request.POST['buyCurrency']
            addStockOperation(account, buyTiker, buyQuantity, buyAvgPrice, buyCurrency, type='buy')

        if 'sellTiker' in request.POST:
            sellTiker = request.POST['sellTiker']
            sellQuantity = request.POST['sellQuantity']
            sellAvgPrice = request.POST['sellAvgPrice']
            sellCurrency = request.POST['sellCurrency']
            addStockOperation(account, sellTiker, sellQuantity, sellAvgPrice, sellCurrency, type='sell')

        if 'transSum' in request.POST:
            transSum = request.POST['transSum']
            fromAcc = request.POST['fromAcc']
            toAcc = request.POST['toAcc']
            addTransfer(FinancialInstrument.objects.get(pk=fromAcc), FinancialInstrument.objects.get(pk=toAcc), transSum)

        if 'addCurrency' in request.POST:
            currency = request.POST['addCurrency']
            addCurrencyToBrokerAccount(account, currency)

    balance, stocks, money, currencys, sumDelta, percentageDifference = getBrokerAccountBalanceStructureCurrency(account)
    color = 'green' if sumDelta >= 0 else 'red'
    account, balance, sumDelta, percentageDifference = brokerAccountsFormat((account,), (balance,), (sumDelta,), (percentageDifference,))
    account = account[0]
    balance = balance[0]
    sumDelta = sumDelta[0]
    percentageDifference = percentageDifference[0]
    CURRENCY_TYPES = FinancialInstrument.CURRENCY_TYPES
    accountsForTransfer = getAccountsForTransfer(request)
    stocksTable = getContractStocksInfo(account, stocks, money)
    context = {'account': account, 'balance': balance, 'CURRENCY_TYPES': CURRENCY_TYPES, 'stocks': stocks,
               'sumDelta': sumDelta, 'percentageDifference': percentageDifference, 'color': color,
               'money': money, 'moneyQ': len(money), 'accountsForTransfer': accountsForTransfer, 'currencys': currencys,
               'stocksTable': stocksTable}
    return render(request, 'accounting/brokerAccount.html', context=context)

def newAccountView(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST' and request.user.is_authenticated:
        if 'bsName' in request.POST:
            bsName = request.POST['bsName']
            bsBalance = request.POST['bsBalance']
            bsCurrency = request.POST['bsCurrency']
            bankName = request.POST['bankName']
            addBankAccount(request, bankName, bsName, bsCurrency, bsBalance)

        if 'isName' in request.POST:
            isName = request.POST['isName']
            isBalance = request.POST['isBalance']
            isCurrency = request.POST['isCurrency']
            brokerName = request.POST['brokerName']
            addBrokerAccount(request, brokerName, isName, isCurrency, isBalance)

    banks = Bank.objects.all()
    CURRENCY_TYPES = FinancialInstrument.CURRENCY_TYPES
    bankAccounts = getBankAccounts(request)
    bankAccountsNum = len(bankAccounts)
    brokerAccounts, balances, sumDelta, percentageDifference = getBrokerAccounts(request)
    brokerAccountsNum = len(brokerAccounts)
    brokerAccounts, balances = brokerAccountsFormat(brokerAccounts, balances, sumDelta, percentageDifference)
    bankAccounts, colors = bankAccountFormat(bankAccounts)
    brokerAccountsBalance = zip(brokerAccounts, balances)
    bankAccountsColor = zip(bankAccounts, colors)
    context = {'banks': banks, 'CURRENCY_TYPES': CURRENCY_TYPES, 'bankAccountsNum': bankAccountsNum,
               'brokerAccountsNum': brokerAccountsNum, 'bankAccountsColor': bankAccountsColor, 'brokerAccountsBalance': brokerAccountsBalance}
    return render(request, 'accounting/newAccount.html', context=context)

def bankAccountsView(request):
    if request.user.is_anonymous:
        return redirect('login')
    bankAccounts = getBankAccounts(request)
    bankAccountsNum = len(bankAccounts)
    accountsNum = bankAccountsNum
    if accountsNum >= 2:
        totalBalance = getTotalBalance(request, bankAccounts, [], [])
        totalBalance, totalBalanceColor = totalBalanceFormat(totalBalance)
    else:
        totalBalance = None
        totalBalanceColor = None
    bankAccounts, colors = bankAccountFormat(bankAccounts)
    bankAccountsColor = zip(bankAccounts, colors)
    incomes = getAllIncomes(request)
    spendings = getAllSpending(request)
    title = 'Банковские счета'
    context = {'totalBalance': totalBalance, 'totalBalanceColor': totalBalanceColor, 'bankAccounts': bankAccountsColor, 'accountsNum': accountsNum,
               'spendings': spendings, 'incomes': incomes, 'title': title, 'bankActive': 'active'}
    return render(request, 'accounting/accounts.html', context=context)


def brokerAccountsView(request):
    if request.user.is_anonymous:
        return redirect('login')
    brokerAccounts, brokerBalances, sumDelta, percentageDifference = getBrokerAccounts(request)
    brokerAccountsNum = len(brokerAccounts) + (1 if brokerAccounts[0].currency != 'RUB' else 0)
    accountsNum = brokerAccountsNum
    if accountsNum >= 2:
        totalBalance = getTotalBalance(request, [], brokerAccounts, brokerBalances)
        totalBalance, totalBalanceColor = totalBalanceFormat(totalBalance)
    else:
        totalBalance = None
        totalBalanceColor = None
    brokerAccounts, brokerBalances, _, _ = brokerAccountsFormat(brokerAccounts, brokerBalances, sumDelta, percentageDifference)
    brokerAccountsBalance = zip(brokerAccounts, brokerBalances)
    print(brokerAccounts, brokerBalances)
    title = 'Брокерские счета'
    context = {'totalBalance': totalBalance, 'totalBalanceColor': totalBalanceColor,
               'brokerAccountsNum': brokerAccountsNum, #'bankAccountsColor': bankAccountsColor,
               'brokerAccountsBalance': brokerAccountsBalance, 'accountsNum': accountsNum, 'brokerActive': 'active',
               'title': title}
    return render(request, 'accounting/accounts.html', context=context)