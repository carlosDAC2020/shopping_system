from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def index(request):
    return render(request, "sales/index.html")  

def signup(request):
    if request.method=="GET":
        return render(request,"sales/signup.html",{
            "form":UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request,user)
                return redirect("sales:home")
            except IntegrityError: 
                return render(request,"sales/signup.html",{
                    "form":UserCreationForm,
                    "mensaje":"usuario ya existente "
                })
        return render(request,"sales/signup.html",{
            "form":UserCreationForm,
            "mensaje":"las contraseñas no coinciden "
        })

def home(request):
    return render(request,"sales/home.html")

def end_sesion(request):
    logout(request)
    return redirect("sales:index")

def signin(request):
    if request.method=="GET":
        return render(request,"sales/signin.html",{
            "form":AuthenticationForm
        })
    else:
        user = authenticate(
            request, 
            username = request.POST["username"], 
            password = request.POST["password"])
        if user == None:
            return render(request,"sales/signin.html",{
            "form":AuthenticationForm,
            "mensaje":" usuario o contraseña incorrectos"
        })
        else:
            login(request,user)
            return redirect("sales:home")
