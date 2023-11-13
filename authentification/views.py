from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db import connection
from django.contrib.auth.hashers import make_password
from datetime import datetime



# Create your views here.
def home(request):
    return render(request,"authentification/index.html")



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

       #flow 1 solution:Broken Access Control 
       #if User.objects.filter(email=email).exists():
       #messages.error(request, 'An account with this email address already exists.')
       #return redirect('signup')
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hashed_password = make_password(pass1)
        query = f"INSERT INTO auth_user (username, first_name, last_name, email, password, is_superuser, is_staff, is_active, date_joined) VALUES ('{username}', '{fname}', '{lname}', '{email}', '{hashed_password}', 0, 0, 1, '{date_joined}')"
        with connection.cursor() as cursor:
            cursor.execute(query)
        #flow2 solution:Sql Injection 
        #myuser= User.objects.create_user(username, email, pass1)
        #myuser.first_name = fname
        #myuser.last_name = lname
        #myuser.save()

        messages.success(request, "Your account has been successfully created")
        return redirect('signin')

    return render(request, "authentification/signup.html")
def signin(request):
    if request.method == 'POST':
       username=request.POST['username']
       pass1=request.POST['pass1']
       user=authenticate(username=username,password=pass1)
       if user is not None:
          login(request, user)
          fname=user.first_name
          return render(request, 'authentification/index.html',{'fname':fname})
       else:
          messages.error(request, 'Invalid username or password')
          return redirect('home')

    return render(request,"authentification/signin.html")

def signout(request):
 
 logout(request)
 messages.success(request,"Logged Out Successfully")
 return redirect('home')