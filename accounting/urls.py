"""diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('bank-accounts/', views.bankAccountsView, name='bank-accounts-page'),
    path('broker-accounts/', views.brokerAccountsView, name='broker-accounts-page'),
    path('bank-accounts/<int:pk>', views.bankAccountView, name='bank-accounts'),
    path('broker-accounts/<int:pk>', views.brokerAccountView, name='broker-accounts'),
    path('new-account', views.newAccountView, name='new-account'),
]
