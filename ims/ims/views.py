from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render (request, 'home.html',{})


def addArticle(request):
    return render(request, 'addArticle.html')


def showInventory(request):
    return render(request, 'showInventory.html')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'home.html')


def register(request):
    return render(request,'register.html')