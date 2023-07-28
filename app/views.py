from django.shortcuts import render, redirect

# Create your views here.

def toIndex(request):
    return redirect('homepage')


def login_page(request):
    
    return render(request, 'index/login.html')


def homepage(request):
    print(request.session.keys())
    if '_auth_user_id' not in request.session.keys():
        return redirect('login-page')
    

    return render(request, 'index/homepage.html')

def show_product(request):
    if '_auth_user_id' not in request.session.keys():
        return redirect('login-page')
    return render(request, 'product/show.html')

def create_product(request):
    if '_auth_user_id' not in request.session.keys():
        return redirect('login-page')
    return render(request, 'product/create.html')


def show_shop(request):
    if '_auth_user_id' not in request.session.keys():
        return redirect('login-page')
    return render(request, 'shop/show.html')

def create_shop(request):
    
    return render(request, 'shop/create.html')