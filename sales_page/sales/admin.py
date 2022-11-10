from django.contrib import admin
from .models import Invoice, Product, Client, Sale

class ClientAdmin(admin.ModelAdmin):
    fields=["first_name","last_name","username","password","email","phone","balance"]
    list_display=["first_name","last_name","date_joined"]
    list_filter=["date_joined"]
    search_fields=["first_name","last_name"]

admin.site.register(Client, ClientAdmin)

#---------------------------------------------------------------------------------------

class InvoiceAdmin(admin.ModelAdmin):
    list_display=["pk","id_client","worth_invoice","date_invoice","status_payment"]
    list_filter=["date_invoice"]

admin.site.register(Invoice, InvoiceAdmin)

#---------------------------------------------------------------------------------------

class ProductAdmin(admin.ModelAdmin):
    list_display=["pk","name","units_available","worth_unit"]

admin.site.register(Product, ProductAdmin)

#---------------------------------------------------------------------------------------
class SaleAdmin(admin.ModelAdmin):
    list_display=["pk","id_invoice","id_product","units_product","worth_sale"]

admin.site.register(Sale, SaleAdmin)