from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *



def index(request):
    return render(request, 'register.html')

def jump_toLogin(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/products')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/products')

def logout(request):
    request.session.clear()
    return redirect('/')

def products(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id = request.session['user_id'])
    context = {
		"user": user,
        # "user_products": Product.objects.filter(user=user),
        "products": Product.objects.all()
	}
    return render(request,"dashboard.html",context)

def new(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request,"new.html",context)

def create(request):
    if request.method == "POST":
        errors = Product.objects.validate(request.POST)
        if errors:
            # for e in errors.items():
            #     messages.error(request, e)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/products/new")
        Product.objects.create(
            product_name=request.POST['product_name'],
            description =request.POST['description'],
            condition =request.POST['condition'],
            # product_img = request.POST['product_img'],
            user=User.objects.get(id=request.session['user_id'])
        )
    return redirect("/products")

def detail(request, id):
    product = Product.objects.get(id=id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "user" :user,
        "product": product,
		# "product_user":Product.objects.all().exclude(user=user)
    }
    return render(request,'product_detail.html', context)

def edit(request, id):
    product = Product.objects.get(id=id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        "to_update": product,
        "user": user
    }
    return render(request, "edit.html", context)

def update(request, id):
    to_update = Product.objects.get(id=id)
    to_update.product_name = request.POST["update_product_name"]
    to_update.description = request.POST["update_description"]
    to_update.condition= request.POST["update_condition"]
    to_update.save()
    return redirect(f"/products/detail/{id}")

def delete(request,id):
    product = Product.objects.get(id=id)
    product.delete() 
    return redirect("/products")

# def interest(request,id):
#     user = User.objects.get(id=request.session['user_id'])
#     product = Product.objects.get(id=id)
#     user.products.add(product)
#     return redirect("/products")

# def cancel(request,id):
#     user = User.objects.get(id=request.session['user_id'])
#     product = Product.objects.get(id=id)
#     user.products.remove(product)
#     return redirect("/products")