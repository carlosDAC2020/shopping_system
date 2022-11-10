from django.urls import path
from . import views

app_name="sales"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("logout/", views.end_sesion, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("<int:product_id>/add_sales/", views.add_sales, name="add_sales"),
    path("<int:id_sale>/delete_sale/", views.delete_sales, name="delete_sale"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("pay/", views.pay, name="pay"),
    path("<int:id_invoice>/invoice_detail/", views.invoice_detail, name="invoice_detai"),
]