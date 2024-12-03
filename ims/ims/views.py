from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Lager  # Make sure to import your Lager model


def home(request):
    return render (request, 'home.html',{})


def addArticle(request):
    return render(request, 'addArticle.html')


def showInventory(request):
    lager = Lager.objects.all()
    return render(request, 'showInventory.html', {'lager': lager})



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

def addArticleData(request):
    if request.method =="POST":
        barcode = request.POST.get('Barcode')
        bezeichnung = request.POST.get('Bezeichnung')
        kategorie = request.POST.get('Kategorie')
        lagerbestand = request.POST.get('Lagerbestand')
        mindestbestand = request.POST.get('Mindestbestand')

        # Create a new Article in the database and store it into the table Lager
        article = Lager(Barcode=barcode, Bezeichnung=bezeichnung, Kategorie = kategorie, Lagerbestand = lagerbestand, Mindestbestand = mindestbestand)
        article.save()

        return redirect('home')
    else:
        return HttpResponse("Invalid request method.")
    

@require_POST
def deleteArticle(request):
    if request.POST.get('action') == 'post':
        try:
            article_id = int(request.POST.get('product_id'))
            article = Lager.objects.get(id=article_id)
            article.delete()
            return JsonResponse({'success': True, 'article_id': article_id})
        except Lager.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Article not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)