from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Lager

from django.db.models import F

def home(request):
    return render (request, 'home.html',{})


def addArticle(request):
    unique_categories = Lager.objects.values_list('Kategorie', flat=True).distinct()
    context = {'categories': unique_categories}
    return render(request, 'addArticle.html', context)
  


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

@require_POST
def minusOne(request):
    if request.POST.get('action') == 'post':
        try:
            article_id = int(request.POST.get('product_id'))
            updated = Lager.objects.filter(id=article_id, Lagerbestand__gt=0).update(Lagerbestand=F('Lagerbestand') - 1)
            if updated:
                return JsonResponse({'success': True, 'article_id': article_id})
            else:
                return JsonResponse({'success': False, 'error': 'Article not found or quantity already zero'}, status=400)
            
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid article ID'}, status=400)
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
