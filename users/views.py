from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from pytz import timezone
from datetime import datetime
from django.http import QueryDict
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

def gauth(request):
    session_store = SessionStore()
    # print(request.body.decode('utf-8'))
    request.session = session_store
    if request.method == 'POST':
        jwt = request.POST.get('jwt')
        decoded = decode_jwt(jwt)
        username = decoded['sub']
        type(username)
        password = username+"googleuser"+decoded['sub']
        fname = decoded['given_name']
        lname = decoded['family_name']
        if not User.objects.filter(username=username).exists():
            gsignup(request, username, password, fname, lname)
        else:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('datavalidation:index')
        # return JsonResponse({"status": "success"})

def gsignup(request, username, password, fname, lname):
    new = QueryDict('', mutable=True)
    new.appendlist('username', username)
    new.appendlist('first_name', fname)
    new.appendlist('last_name', lname)
    new.appendlist('password1', password)
    new.appendlist('password2', password)
    form = CustomUserCreationForm(new)
    if form.is_valid():
        user = form.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect("datavalidation:index")

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.InvalidTokenError as e:
        print("Error decoding JWT token:", e)
        return None