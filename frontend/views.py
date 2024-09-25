from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth import login, authenticate, login as auth_login
from django import forms
from django.contrib.auth.forms import AuthenticationForm



#--------------------------------------------------- Productos ------------------------------------------------------------------

def home(request):
    return redirect('product_list')

# Listar productos
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# Crear producto
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

# Actualizar producto
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

# Eliminar producto
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


#----------------------------------------------------- Subastas --------------------------------------------------------------------

def auction_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.product = product
            auction.current_price = auction.starting_price
            auction.save()
            return redirect('auction_list')
    else:
        form = AuctionForm()
    return render(request, 'products/auction_form.html', {'form': form, 'product': product})

# Listar subastas activas
def auction_list(request):
    auctions = Auction.objects.filter(bid_end_time__gt=timezone.now())
    return render(request, 'products/auction_list.html', {'auctions': auctions})


#----------------------------------------------Carrito de compras ------------------------------------------------------------------

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        item, created = Item.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'price_at_purchase': product.price, 'quantity': 1}
        )
        if not created:
            item.quantity += 1  # Aumentar la cantidad si el producto ya está en el carrito
            item.save()

    return redirect('product_list')  # Redirigir a la lista de productos o a otra página

# views.py
def view_cart(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'products/view_cart.html', {'items': items})


def update_cart_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    new_quantity = request.POST.get('quantity')
    if new_quantity and new_quantity.isdigit() and int(new_quantity) > 0:
        item.quantity = int(new_quantity)
        item.save()
    return redirect('view_cart')

def remove_cart_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')


#------------------------------------------------- Autenticación ------------------------------------------------------------------

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión al usuario después del registro
            return redirect('product_list')  # Redirige a la lista de productos
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('product_list')  # Redirigir a la lista de productos
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})


#--------------------------------------------------- Comentarios ------------------------------------------------------------------

def product_list(request):
    products = Product.objects.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Asignar el usuario actual al comentario
            comment.product = Product.objects.get(id=request.POST.get('product_id'))
            comment.save()
            return redirect('product_list')

    return render(request, 'products/product_list.html', {
        'products': products,
        'comment_form': comment_form
    })