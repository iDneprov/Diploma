from .models import Bank, FinancialInstrument
from django.forms import ModelForm, TextInput, ImageField


class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'image']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Название банка"
            }),

        }


class Bank(ModelForm):
    class Meta:
        model = FinancialInstrument
        fields = ['name', 'currency']
