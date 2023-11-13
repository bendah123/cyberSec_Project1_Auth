from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


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

        #if User.objects.filter(email=email).exists():
         #  messages.error(request, 'An account with this email address already exists.')
           #return redirect('signup')
        query = f"INSERT INTO auth_user (username, first_name, last_name, email, password) VALUES ('{username}', '{fname}', '{lname}', '{email}', '{pass1}')"
        User.objects.raw(query)

    

        myuser= User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your Account has been successfully created")
        return redirect('signin')

    return render(request,"authentification/signup.html")

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