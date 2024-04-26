from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import F
from .forms import LoginForm, UserRegistrationForm, ProductForm, ProfileForm
from .models import User, Product, CartItem


def home(request):
    return render(request, 'shop/home.html')


def user_login(request, msg=None):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Invalid credentials')
        else:
            msg = 'form validation error'
    return render(request, 'shop/login.html', {'form': form, 'msg': msg})


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    msg = None
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.errors)
            user = form.save()
            messages.success(request, "user created")
            return redirect('login')
        else:
            msg='form is not valid'
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form, 'msg': msg})


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_staff:
            return redirect('admin:index')
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            form = ProfileForm(instance=user)
        return render(request, 'shop/profile.html', {'form': form})
    else:
        return redirect('login')
    

def catalog(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            products = Product.objects.all().order_by('name')
        elif request.user.user_type == 2:
            # If user is a seller, filter products by seller ID
            products = Product.objects.filter(seller=request.user).order_by('name')
        else:
            # If user is a customer, display all products
            products = Product.objects.all().order_by('name')
            cart = CartItem.objects.filter(user=request.user)
    else:
        products = Product.objects.all().order_by('name')  # Handle anonymous user case
    
    return render(request, 'shop/catalog.html', {'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Assuming the form submits the quantity to be added to the cart
        quantity = int(request.POST.get('quantity', 1))
        if product.remaining >= quantity:
            # Update remaining quantity
            product.remaining -= quantity
            request.user.add_to_cart(product, quantity)
            product.save()
            request.user.save()
            # Here you can implement additional logic to add the product to the cart
    return redirect('catalog')  # Redirect back to the products page


def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('catalog')  # Redirect back to the products page


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the seller to the currently authenticated user
            product.save()
            return redirect('catalog')  # Redirect to a relevant page after adding the product
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})


def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog')  # Redirect to a relevant page after updating the product
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/update_product.html', {'form': form, 'product': product})


def cart(request):
    cart = CartItem.objects.filter(user=request.user)
    print(cart)
    return render(request, 'shop/cart.html', {'cart': cart})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    product = item.product
    Product.objects.filter(pk=product.pk).update(remaining=F('remaining') + item.quantity)
    item.delete()
    return redirect('cart')