from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addArticle/', views.addArticle, name='addArticle'),
    path('showInventory/', views.showInventory, name='showInventory'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('addArticleData/', views.addArticleData, name= 'addArticleData')
    
]
