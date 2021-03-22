from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests import request
from store.views import *
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
        else:
            messages.success(request, 'Enter Your Details Correctly')

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)
    return redirect('login-page')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password2 = request.POST.get('password2')

        user = authenticate(request, username=username, password=password2)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, 'Username OR Password is incorrect')

    return render(request, 'accounts/login.html')


