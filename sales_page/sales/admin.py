from django.contrib import admin
from .models import Invoice, Product, Client

class ClientAdmin(admin.ModelAdmin):
    fields=["first_name","last_name","username","password","email","phone","balance"]
    list_display=["first_name","last_name","date_joined"]
    list_filter=["date_joined"]
    search_fields=["first_name","last_name"]

admin.site.register(Client, ClientAdmin)

admin.site.register(Invoice)

admin.site.register(Product)

