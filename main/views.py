from django.shortcuts import render, redirect, get_object_or_404
from accounting.operations import addBankAccount, addOperation, addTransfer, getUserOperations, getBankAccounts, \
    floatFormating, getBankAccountOperations, getCurrencySymbols, getAccountsForTransfer, accBallanceList, \
    getAllSpending, getAllIncomes, getBrokerAccounts, bankAccountFormat, brokerAccountsFormat, getTotalBalance,\
    totalBalanceFormat
from accounting.models import FinancialInstrument, Category, Operation


def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    bankAccounts = getBankAccounts(request)
    bankAccountsNum = len(bankAccounts)
    brokerAccounts, brokerBalances, sumDelta, percentageDifference = getBrokerAccounts(request)
    brokerAccountsNum = len(brokerAccounts)
    accountsNum = bankAccountsNum + brokerAccountsNum
    if accountsNum >= 2:
        totalBalance = getTotalBalance(request, bankAccounts, brokerAccounts, brokerBalances)
        totalBalance, totalBalanceColor = totalBalanceFormat(totalBalance)
    else:
        totalBalance = None
        totalBalanceColor = None
    brokerAccounts, brokerBalances, _, _ = brokerAccountsFormat(brokerAccounts, brokerBalances, sumDelta, percentageDifference)
    bankAccounts, colors = bankAccountFormat(bankAccounts)
    brokerAccountsBalance = zip(brokerAccounts, brokerBalances)
    bankAccountsColor = zip(bankAccounts, colors)
    incomes = getAllIncomes(request)
    spendings = getAllSpending(request)
    context = {'totalBalance': totalBalance, 'totalBalanceColor': totalBalanceColor, 'bankAccounts': bankAccountsColor, 'brokerAccountsBalance':brokerAccountsBalance, 'accountsNum': accountsNum,
               'spendings': spendings, 'incomes': incomes}
    return render(request, 'accounts.html', context=context)

