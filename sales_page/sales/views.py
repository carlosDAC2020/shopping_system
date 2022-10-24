from itertools import product
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Client, Invoice, Sale, Product

def index(request):
    products = Product.objects.all()
    return render(request, "sales/index.html",{
        "products":products
    })  

def signup(request):
    if request.method=="GET":
        return render(request,"sales/signup.html")
    else:
        # verificamos que las contraseñas coincidan
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # registramos el usuario nuevo 
                user = Client.objects.create_user(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                phone=request.POST["phone"],
                username=request.POST["username"], 
                password=request.POST["password1"])
                user.save()
                # le damos un login automantico al usuario
                login(request,user)
                return redirect("sales:home")
            # en caso de que el usuario ya este registrado elevamos el error de integridad 
            except IntegrityError: 
                return render(request,"sales/signup.html",{
                    "mensaje":"usuario ya existente "
                })
        return render(request,"sales/signup.html",{
            "mensaje":"las contraseñas no coinciden "
        })

def home(request, ):
    products = Product.objects.all()
    return render(request,"sales/home.html",{
        "products":products
    })

def end_sesion(request):
    logout(request)
    return redirect("sales:index")

def signin(request):
    if request.method=="GET":
        return render(request,"sales/signin.html")
    else:
        user = authenticate(
            request, 
            username = request.POST["username"], 
            password = request.POST["password"])
        if user == None:
            return render(request,"sales/signin.html",{
            "mensaje":" usuario o contraseña incorrectos"
        })
        else:
            login(request,user)
            return redirect("sales:home")
