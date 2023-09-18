from django.urls import path
from . import views as app
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

urlpatterns = [
    path('', app.homepage, name='homepage'),
    path('login/', app.login, name='login'),
    
    
    # shop
    path('shop/product-all', app.shopProducts, name='shop-products-page'),
    path('shop/input-invoice', app.shopInvoice, name='shop-invoice-page'),
    path('shop/data-input', app.dataInput, name='shop-data-input-page'),
]
