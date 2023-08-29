from django.shortcuts import render, redirect

# Create your views here.

def toIndex(request):
    
    return redirect('homepage')

def login_page(request):
    
    return render(request, 'index/login.html')

def homepage(request):
    try :
        
        if request.session['_auth_user_id'] == None:
            pass
        
    except :
        
        return redirect('login-page')
    return render(request, 'index/homepage.html')

def show_product(request):
    
    return render(request, 'product/show.html')

def create_product(request):

    return render(request, 'product/create.html')

def show_shop(request):
    
    return render(request, 'shop/shop_show.html')

def create_shop(request):
    
    return render(request, 'shop/shop_create.html')