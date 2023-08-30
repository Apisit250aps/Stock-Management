from django.urls import path
from . import views as app
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

urlpatterns = [
    path('index/', app.homepage, name='homepage'),
    path('login/', app.login_page, name='login-page'),
    path('product/', app.show_product, name='show-product-page'),
    path('product/create/', app.create_product, name='create-product-page'),
    path('shop/', app.show_shop, name='show-shop-page'),
    path('shop/create/', app.create_shop, name='create-shop-page'),
    path('logout',logout , name='logout')
]
