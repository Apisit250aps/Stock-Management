from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def getUser(request):

    return request.user.is_authenticated


@login_required(login_url='/login/')
def homepage(request):

    return render(request, 'shop/base.html')

# public


def products(request):

    return render(request, 'public/products.html')


def shops(request):

    return render(request, 'public/shops.html')



# authentications
def login(request):

    return render(request, 'authentications/login.html')

def LOGOUT(request):
    
    logout(request)
    return redirect("index")

def register(request):

    return render(request, 'authentications/register.html')

@login_required(login_url='/login/')
def createShop(request):

    return render(request, 'authentications/create-shop.html')



# shop
@login_required(login_url='/login/')
def shopInvoice(request):

    return render(request, 'shop/input-invoice.html')

@login_required(login_url='/login/')
def shopInputData(request):

    return render(request, 'shop/input-data.html')

@login_required(login_url='/login/')
def shopProducts(request):

    return render(request, 'shop/all-product.html')

@login_required(login_url='/login/')
def dataInput(request):

    return render(request, 'shop/add-new.html')
