
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Client, Invoice, Sale, Product
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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


@login_required
def home(request, ):
    products = Product.objects.all()
    return render(request,"sales/home.html",{
        "products":products
    })


@login_required
def end_sesion(request):
    logout(request)
    return redirect("sales:index")


@login_required
def add_sales(request,product_id):
    # traemos la ultima factura regiatrada 
    invoice_most_recently = Invoice.objects.order_by("-date_invoice")[:1]
     # seleccionamos el producto a comprar
    product = Product.objects.get(pk=product_id)

    # en caso de que la ultima factura se haya registrado en los ultimos 30 minutos y su estado de pogo sea falso
    # se añadira la venta correspondiente a dicha factura 
    if invoice_most_recently[0].invoice_most_recently():
        # craemos la venta y la asociamos  con la factura creada anteriormente 
        new_sale = Sale.objects.create(id_invoice=invoice_most_recently[0], id_product=product)
        new_sale.save()
    
    
    else:
        # creamos la factura
        new_invoice = Invoice.objects.create(date_invoice=timezone.now(), id_client=request.user)
        # guardamos la factura
        new_invoice.save()
        # añadimos la venta a una nueva factura
        new_sale = Sale.objects.create(id_invoice=new_invoice, id_product=product)
        new_sale.save()
   
    return redirect("sales:home")



