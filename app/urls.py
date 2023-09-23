from django.urls import path
from . import views as app
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

urlpatterns = [
    # public
    path('', app.products, name='index'),
    path('shop', app.shops, name='shop'),
    
    
    # authentications
    path('login/', app.login, name='login'),
    path('register/', app.register, name='register'),
    path('create-shop/', app.createShop, name='create-shop-page'),
    path('logout', app.LOGOUT, name='logout'),
    
    # shop
    path('shop/product-all', app.shopProducts, name='shop-products-page'),
    path('shop/input-invoice', app.shopInvoice, name='shop-invoice-page'),
    path('shop/add-product', app.dataInput, name='shop-data-input-page'),
    path('shop/input-data', app.shopInputData, name='shop-input-data-page'),
    
    # account
    path('account/account', app.Account, name='account-page')
]
