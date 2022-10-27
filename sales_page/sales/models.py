import datetime

from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(User):
    phone = models.IntegerField(default=0)
    balance = models.IntegerField(default=50000)

    def __str__(self):
        return self.username
    
    def balance_print(self):
        return str(self.balance)


class Product(models.Model):# tabla productos 
    # columna             # tpos de datos 
    name = models.CharField(max_length=20)
    units_available = models.IntegerField(default=0)
    worth_unit = models.IntegerField(default=0)
    photo_product = models.ImageField(upload_to='media/images/', default="media/images/")
    
    def __str__(self):
        return self.name 


class Invoice(models.Model):# tabla recivos
    # columna             # tpos de datos 
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    worth_invoice = models.IntegerField(default=0)
    date_invoice = models.DateTimeField(" date invoice ")
    status_payment = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.pk)

    def invoice_most_recently(self):
        return self.date_invoice >= timezone.now() - datetime.timedelta(minutes=30) and self.status_payment==False


class Sale(models.Model):# tabla ventas
    # columna             # tpos de datos 
    id_invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units_product = models.IntegerField(default=0)
    worth_sale = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)