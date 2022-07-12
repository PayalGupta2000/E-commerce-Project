from django.urls import path
from . import views

urlpatterns=[
    path("home/",views.home),
    path("brands/",views.Brands),
    path("",views.products),
    path("delete/",views.delete),
    path("add_new_product/",views.addNewProduct),
    path("add_new_brand/",views.addBrandName),
    path("save_brand",views.save_brand),
    path("save_product",views.save_product),
    path("save_user",views.save_user),
    path("add_cart",views.addToCart),
    path("login",views.validate_user),
    path("logout/",views.logout),
    path("cart/",views.cart),
    path("category/",views.category),
    path("plus/",views.cart_plus),
    path("minus/",views.cart_minus),
    path("desc/",views.desc),
    path("purchase/",views.purchase, name="purchase"),
    path("paymenthandler/",views.paymenthandler,name="paymenthandler"),
]