from django.urls import path
from . import views as api
from django.shortcuts import render, redirect

urlpatterns = [
    path('get/province', api.getProvince, name='get-province'),
    path('get/district', api.getDistrict, name='get-district'),
    path('get/sub-district', api.getTambon, name='get-subDistrict'),
    path('get/area', api.getArea, name='get-area'),
    path('get/product-type', api.getProductType, name='get-product-type'),
    path('get/product-categories', api.getProductCategory, name='get-product-categories'),
    path('get/invoice/shop', api.getShopInputInvoices, name='get-invoice-shop'),
    
    # authentication
    path('get/user/id', api.get_user, name='get-user-id'),
    path('auth-login/', api.login_api,name='login-api'),
    path('auth-register/', api.register_api,name='register-api'),
    path("user-check", api.userCheck, name='user-check-api'),
    path('create-shop', api.createShop, name='create-shop-api'),
    
    # shop
    path('get/product/all', api.getAllProductData, name="get-product-all"),
    path('get/product/shop', api.getProductShop, name="get-product-shop"),
    path('get/shop/all', api.getAllShop, name='get-shop-all'),
    path('create-InputData', api.createInputData, name='create-InputData-api'),
    path('edit/product/', api.editProduct, name='edit-product-api'),
    path('edit/shop/', api.editShop, name='edit-shop-api'),
    path('delete/product/', api.deleteProduct, name='delete-product-api'),
    path('delete/shop/', api.deleteShop, name='delete-shop-api'),

]
