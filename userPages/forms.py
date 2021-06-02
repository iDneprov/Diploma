from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, PasswordInput


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['login', 'password']
        widgets = {
            'login': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Логин"
            }),
            'password': PasswordInput(attrs={
                'class': "form-control",
                'placeholder': "Пароль"
            })
        }