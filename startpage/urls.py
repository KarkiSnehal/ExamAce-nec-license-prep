from django.contrib import admin
from django.urls import path
from startpage import views  

urlpatterns = [
    path('', views.home, name='start'),
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    

]
