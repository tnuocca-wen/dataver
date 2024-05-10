from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from pytz import timezone
from datetime import datetime
from django.http import QueryDict
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import jwt


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('datavalidation:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return render(request, 'users/login.html', {'message': "Invalid Username"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            with open("../logs/login.log", "a+", encoding="utf-8") as log:
                log.seek(0)
                if len(log.read()) != 0:
                    log.write("\n" + str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')) + "   " + username)
                else:
                    log.write(str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')) + "   " + username)
                log.close()
            return redirect("datavalidation:index")
        else:
            return render(request, 'users/login.html', {'message': "Invalid Password"})
    else:
        return render(request, 'users/login.html', {})

def signup_view(request):
    if request.method == 'POST':
        print(request.session)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            with open("../logs/signup.log", "a+", encoding="utf-8") as log:
                log.seek(0)
                if len(log.read()) != 0:
                    log.write("\n" + str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')) + "   " + username + "    " + password)
                else:
                    log.write(str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')) + "   " + username + "    " + password)
                log.close()
            return redirect("datavalidation:index")#render(request, 'users/login.html', {"message": "Account created successfully"})  # Replace 'home' with the URL name of your home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')

@csrf_exempt
def gauth(request):
    if request.method == 'POST':
        csrf_token_cookie = request.COOKIES.get('g_csrf_token')
        if not csrf_token_cookie:
            print('No CSRF token in Cookie.')
            return render(request, 'users/login.html', {'message':'Login Failed'})
        csrf_token_body = request.POST['g_csrf_token']
        if not csrf_token_body:
            print('No CSRF token in POST body.')
            return render(request, 'users/login.html', {'message':'Login Failed'})
        if csrf_token_cookie != csrf_token_body:
            print('Failed to verify double submit cookie')
            return render(request, 'users/login.html', {'message':'Login Failed'})
        print(csrf_token_cookie, csrf_token_body)
        jwt = request.POST['credential']
        # print(jwt)
        try:
            decoded = id_token.verify_oauth2_token(
            jwt, requests.Request(), os.getenv('CLIENT_ID'))
            # print(decoded)
            if decoded:
                username = decoded['sub']
                email = decoded['email']
                password = username+"googleuser"+decoded['sub']
                fname = decoded['given_name']
                lname = decoded['family_name']
                if not User.objects.filter(username=username).exists():
                    gsignup(request, username, email, password, fname, lname)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    with open("../logs/login.log", "a+", encoding="utf-8") as log:
                        log.seek(0)
                        if len(log.read()) != 0:
                            log.write("\n" + str(datetime.now()) + "   " + username)
                        else:
                            log.write(str(datetime.now()) + "   " + username)
                        log.close()
                    return redirect('datavalidation:index')
                else:
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    with open("../logs/login.log", "a+", encoding="utf-8") as log:
                        log.seek(0)
                        if len(log.read()) != 0:
                            log.write("\n" + str(datetime.now()) + "   " + username)
                        else:
                            log.write(str(datetime.now()) + "   " + username)
                        log.close()
                    return redirect('datavalidation:index')
            else:
                print("invalid login")
        except:
            print("invalid login")
            return JsonResponse({"status": 400, "message": "invalid login"})

def gsignup(request, username, email, password, fname, lname):
    print("got here")
    new = QueryDict('', mutable=True)
    new.appendlist('username', username)
    new.appendlist('email', email)
    new.appendlist('first_name', fname)
    new.appendlist('last_name', lname)
    new.appendlist('password1', password)
    new.appendlist('password2', password)
    form = CustomUserCreationForm(new)
    if form.is_valid():
        form.save()
    with open("../logs/signup.log", "a+", encoding="utf-8") as log:
        log.seek(0)
        if len(log.read()) != 0:
            log.write("\n" + str(datetime.now()) + "   " + username + "    " + password)
        else:
            log.write(str(datetime.now()) + "   " + username + "    " + password)
        log.close()


def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.InvalidTokenError as e:
        print("Error decoding JWT token:", e)
        return None