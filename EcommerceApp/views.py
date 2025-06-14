import json
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ProductForm, CategoryForm,userLoginForm
from django.contrib import messages
from .models import Product, Cart, Category
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


def admin_required(view_func):  
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,  
        login_url="adminLogin"  
    )(view_func)

def userLogin_required(view_func):  
    return user_passes_test(
        lambda u: u.is_authenticated,  
        login_url="signin"  
    )(view_func)



def signup(request):
    if request.method == "POST":
        form = userLoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"successfully created")
            return redirect('signup')
        else:
            messages.error(request,"Invalid try again!")
            return redirect('signup')
    else:
        form  = userLoginForm()
        context = {
            'form':form
        }
        return render(request, "userLogin/signup.html",context)

def signin(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST['password']
        users = User.objects.filter(username=uname,password=password)
        if users.exists():
            user = User.objects.get(username=uname)
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid Credintial! Please try again!")
            return redirect('signin')
    else:
        return render(request,"userLogin/signin.html")

def userLogout(request):
    auth.logout(request)
    return redirect('signin')

@userLogin_required
def index(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,"index.html",context)


@userLogin_required
def addToCart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
            cartItem, created = Cart.objects.get_or_create(product=product)

            if not created:
                cartItem.quantity += 1
                cartItem.save()
            return JsonResponse({"success":True})
        except Product.DoesNotExist:
            return JsonResponse({"success" : False,"error":"product not found"},status=400)
    return JsonResponse({"success":False},status=400)

       
    

@userLogin_required
def cart(request):
    carts = Cart.objects.all()
    totalPrice = 0
    totalItem = 0
    for cart in carts:
        totalPrice += cart.quantity * cart.product.price
        totalItem += cart.quantity
    
    context = {
        'carts':carts,
        'totalPrice':totalPrice,
        'totalItem':totalItem
    }
    return render(request, "cart.html",context)

def fetchCart(request):
    if request.method == "POST":
        carts = Cart.objects.all()
        totalItem = 0
        for cart in carts:
            totalItem += cart.quantity
        return JsonResponse({"success":True, "totalItem":totalItem})
    
    return JsonResponse({"success":False},status=404)

@userLogin_required
def updateCart(request,id):
    action = request.GET.get('action')
    cart = get_object_or_404(Cart, id=id)
    if action == 'increase':
        cart.quantity += 1
    elif action == 'decrease' and cart.quantity > 1:
        cart.quantity -= 1
    cart.save()
    return redirect('cart')

@userLogin_required
def deleteCart(request,id):
    cart = get_object_or_404(Cart, id=id)
    cart.delete()
    return redirect('cart')


def category(request):
    categories= Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,"category.html",context)

def categoryDisplay(request,id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category_id=id)
    
    context = {
        'products':products,
        'category':category
    }
    return render(request, "categoryDisplay.html", context)


def details(request,id):
    product = get_object_or_404(Product,id=id)
    context = {
        'product':product
    }
    return render(request,"details.html",context)



def adminLogin(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']
        user_auth = auth.authenticate(username=username,password=password)
        if user_auth is not None:
            user = User.objects.get(username=username)
            if user.is_superuser:
                auth.login(request,user)
                return redirect('admin')
            else:
                messages.error(request,"This user is not admin")
                return redirect("adminLogin")
        else:
            messages.error(request,"Invalid Credential")
            return redirect("adminLogin")

        
    else:
        return render(request,"customAdmin/adminLogin.html")


def adminLogout(request):
    auth.logout(request)
    return redirect("adminLogin")

@admin_required
def admin(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,"customAdmin/admin.html",context)

@admin_required
def addProducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.info(request, "added successfully")
            return redirect("addProducts")
    else:
        form = ProductForm()
        return render(request,"customAdmin/addProducts.html",{'form':form})

@admin_required
def editProduct(request,id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        form = ProductForm(request.POST,instance=product)
        if form.is_valid:
            form.save()
            return redirect("admin")
    else:
        product = get_object_or_404(Product,id=id)
        form = ProductForm(instance=product)
        return render(request,"customAdmin/editProduct.html",{'form':form})

@admin_required
def deleteProduct(request,id):
    product = get_object_or_404(Product,id=id)
    product.image.delete()
    product.delete()
    return redirect('admin')




@admin_required
def addCategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            messages.info(request, "added successfully")
            return redirect("addCategory")
    else:
        form = CategoryForm()
        return render(request, "customAdmin/addCategory.html",{'form':form})


@admin_required
def adminCategoryDisplay(request,id):

        category = Product.objects.filter(category_id=id)
        context = {
            'category':category
        }
        return render(request,"customAdmin/adminCategoryDisplay.html",context)