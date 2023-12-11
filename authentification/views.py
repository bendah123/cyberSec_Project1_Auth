from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db import connection
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import re



# Create your views here.
def home(request):
    return render(request,"authentification/index.html")
def Loginpage(request):
    return render(request,"authentification/info.html")

'''Fix:FLOW 5 : A07:2021 - Identification and Authentication Failures
 SO HERE WE ADDED SOME PASSWORD VERIFICATION CONDITIONS 
def validate_password_strength(password):
    # Validate password length
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # Validate uppercase letter
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."

    # Validate lowercase letter
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."

    # Validate digit
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."

    # No validation errors
    return None'''

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        '''Password verification call function to solve flaw 5 
        password_error = validate_password_strength(pass1)
        if password_error: 
           # messages.error(request, password_error)
           # return redirect('signup')'''

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        
        '''FLAW 1 solution:Broken Access Control 
        if User.objects.filter(email=email).exists():
         messages.error(request, 'An account with this email address already exists.')
        return redirect('signup')'''
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #FLAW 4 A02:2021-Cryptographic Failures
        password1 =pass1
        #Solution Flaw 4 
        #password1 = make_password(pass1)
        #FLAW 2 A03:2021:Injection
        query = f"INSERT INTO auth_user (username, first_name, last_name, email, password, is_superuser, is_staff, is_active, date_joined) VALUES ('{username}', '{fname}', '{lname}', '{email}', '{password1}', 0, 0, 1, '{date_joined}')"
        with connection.cursor() as cursor:
            cursor.execute(query)
        '''flaw 2 solution:Sql Injection 
        myuser= User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()'''

        messages.success(request, "Your account has been successfully created")
        return render(request, 'authentification/welcome.html', {'fname': fname})
    return render(request, "authentification/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        # Retrieve the user from the database without password verification
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            #FLAW 3 A05:2021-Security Misconfiguration   
            messages.error(request, "An Error Happened"+ str(e))
            '''SOLUTION FLOW 3:
            messages.error(request, "Invalid username or password. Please try again.")'''
            return redirect('home')

        # Check if the provided password matches the stored password (plaintext)
        #solution FLAW 4
        #if user.check_password(pass1):
        if pass1==user.password:
            login(request, user)
            fname = user.first_name
            return render(request, 'authentification/welcome.html', {'fname': fname})
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('home')

    return render(request, "authentification/signin.html")


def signout(request):
   
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')
