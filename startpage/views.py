# from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from questions.views import questions

# Create your views here.

def home(request):
    # return HttpResponse("<h1>This is the registerpage</h1>")
    
    return render(request,'home.html',{'hlink':'/login'})



def register(request):
    # return HttpResponse("<h1>This is the registerpage</h1>")
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        
        
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')
        
        # make sure password is at least 5 characters long
        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')

        if user_data_has_error:
            return redirect("/register")
    
        else:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
                )
            messages.success(request, 'Account created. Login now')
            return redirect('login')
        
    
    
    return render(request,'register.html')



def loginView(request):
    # return HttpResponse("<h1>This is the loginpage</h1>")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request=request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('questions')
        else:
        # redirect back to the login page if credentials are wrong
         messages.error(request, 'Invalid username or password')
         return redirect('login')
    return render(request, 'login')





