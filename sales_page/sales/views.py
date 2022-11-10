
from django.shortcuts import render, redirect
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
    user=Client.objects.get(pk=request.user.pk) 
    balance=(user.balance)
    balance="{:,.2f}".format(balance)
    print(balance)
    return render(request,"sales/home.html",{
        "products":products,
        "Client":user,
        "blc":balance
    })


@login_required
def end_sesion(request):
    logout(request)
    return redirect("sales:index")


@login_required
def add_sales(request,product_id):

    # traemos la ultima factura regiatrada 
    invoice_most_recently = Invoice.objects.filter(id_client=request.user.pk).order_by("-date_invoice")[:1]
    #invoice_most_recently = Invoice.objects.order_by("-date_invoice")[:1]
    # seleccionamos el producto a comprar
    product = Product.objects.get(pk=product_id)

    # en caso de que la ultima factura se haya registrado en los ultimos 30 minutos y su estado de pogo sea falso
    # se añadira la venta correspondiente a dicha factura 
    if len(invoice_most_recently)>0 and invoice_most_recently[0].invoice_most_recently():
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
@login_required
def delete_sales(request, id_sale):
    sale=Sale.objects.get(pk=id_sale)
    if len(Sale.objects.filter(id_invoice=sale.id_invoice))>0:
        sale.delete()
        if len(Sale.objects.filter(id_invoice=sale.id_invoice))==0:
            inv=Invoice.objects.get(pk=sale.id_invoice.pk)
            inv.delete()
    return redirect("sales:shopping_cart")

@login_required
def shopping_cart(request):
    # traemos la ultima factura regiatrada 
    invoice_most_recently = Invoice.objects.filter(id_client=request.user).order_by("-date_invoice")[:5]
    invoices=[inv for inv in invoice_most_recently if inv.status_payment==True]
    # evaluamos si la ultima factura no se ha pagado
    if len(invoice_most_recently)>0 and invoice_most_recently[0].status_payment==False :

        sales_recently = Sale.objects.filter(id_invoice=invoice_most_recently[0].pk)
        
        return render(request,"sales/cart.html",{
        "sales_recently":sales_recently,
        "invoice_most_recently":invoices
        })
    else:
        print(invoice_most_recently)
        mensaje=" Empty Cart "
        return render(request,"sales/cart.html",{
        "mensaje":mensaje,
        "invoice_most_recently":invoices
    })

@login_required
def pay(request):
    
    invoice_most_recently = Invoice.objects.filter(id_client=request.user).order_by("-date_invoice")[:1]
    sales_recently = Sale.objects.filter(id_invoice=invoice_most_recently[0].pk)
    user_pay=Client.objects.get(pk=request.user.pk) 

    # asigansmos y guardamos los valores de las ventas a demas 
    # de la cantidad de producto
    total_worth_invoice=0
    for sale in sales_recently:
        sale.units_product=int(request.POST[sale.id_product.name])
        sale.worth_sale=sale.units_product*sale.id_product.worth_unit
        total_worth_invoice+=sale.worth_sale

    # validamos si el usuario tiene el sufiente dinero para hacer la compra
    if user_pay.balance<total_worth_invoice:
        products = Product.objects.all()
        return render(request,"sales/home.html",{
            "products":products,
            "mensaje":"insufficient balance",
            "Client":user_pay
        })
        
    else:
        # guarsamos los datos de la venta 
        sale.save()
        # asiganamos los datos del precio toatl a demas
        # del estado de compra 
        inv =  invoice_most_recently[0]
        inv.worth_invoice=total_worth_invoice
        inv.status_payment=True
        inv.save()
        # actualizamos el balance del usuario restandole el valor de la factura 
        user_pay.balance-=inv.worth_invoice
        user_pay.save()

        # restamos las unidades disponibles de los productos 
        for sale in sales_recently:
            product=Product.objects.get(pk=int(sale.id_product.pk))
            product.units_available-=sale.units_product
            product.save()
            
        return render(request, "sales/invoice_detail.html", {
        "sales_recently":sales_recently,
        "invoice":inv
        })
        
    
@login_required
def invoice_detail(request, id_invoice):
    inv=Invoice.objects.get(pk=id_invoice)
    print(inv)
    sales_recently=Sale.objects.filter(id_invoice=inv.pk)
    return render(request, "sales/invoice_detail.html", {
        "sales_recently":sales_recently,
        "invoice":inv
    })

