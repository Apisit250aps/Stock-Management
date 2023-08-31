from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def getUser(request):
    return request.user.is_authenticated


def toIndex(request):

    return redirect('homepage')


def login_page(request):

    return render(request, 'index/login.html')


@login_required(login_url='/page/login/')
def homepage(request):

    return render(request, 'index/homepage.html')

@login_required(login_url='/page/login/')
def show_product(request):

    return render(request, 'product/invoice.html')

@login_required(login_url='/page/login/')
def create_product(request):

    return render(request, 'product/create.html')

@login_required(login_url='/page/login/')
def show_shop(request):

    return render(request, 'shop/shop_show.html')


def create_shop(request):

    return render(request, 'shop/shop_create.html')
