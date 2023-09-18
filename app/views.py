from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def getUser(request):

    return request.user.is_authenticated


# @login_required(login_url='/page/login/')
def homepage(request):

    return render(request, 'shop/base.html')


# authentications
def login(request):
    
    return render(request, 'authentications/login.html')

def register(request):
    
    return render(request, 'authentications/register.html')



# shop
def shopInvoice(request):
    
    return render(request, 'shop/input-invoice.html')

def shopProducts(request):

    return render(request, 'shop/all-product.html')

def dataInput(request):
    
    return render(request, 'shop/data-input.html')
