from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def index(request):
    return redirect('/')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            logout(request)
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/registration.html', context=context)


def logoutRedirect(request):
    logout(request)
    return redirect('/')
