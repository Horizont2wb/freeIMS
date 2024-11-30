from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def home(request):
    return render (request, 'home.html',{})


def addArticle(request):
    return render(request, 'addArticle.html')


def showInventory(request):
    return render(request, 'showInventory.html')



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect  ('home')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'home.html')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #Log in as the authenticated User
            user = authenticate(username=username, password= password)
            login(request,user)
            return redirect('home')
        else:
            return render(request,'register.html', {'form':form})
    else:
        return render(request,'register.html', {'form':form})