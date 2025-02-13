from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import CustomUserCreationForm
import re
from django.contrib.auth import get_user_model
User = get_user_model()


def shop(request):
    """Displays all products available in the shop."""
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def get_or_create_cart(request):
    """Gets or creates a cart for the current user or guest session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get("cart_id")
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    return cart


def clothy4kids(request):
    """Displays products in the 'Kids' category."""
    products = Product.objects.filter(category='kids')
    return render(request, 'clothy4kids.html', {'products': products})


def reviews(request):
    return render(request, 'reviews.html')


def clothy4men(request):
    """Display only Men's Clothes."""
    men_products = Product.objects.filter(category='men')
    return render(request, 'clothy4men.html', {'products': men_products})

def clothy4women(request):
    """Display only Women's Clothes."""
    women_products = Product.objects.filter(category='women')
    return render(request, 'clothy4women.html', {'products': women_products})

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        #Q(description__icontains=query) |
        #Q(brand__icontains=query) |
        Q(category__icontains=query)
    ) if query else Product.objects.all()

    return render(request, 'search_results.html', {'products': products, 'query': query})

@login_required
def add_to_cart(request, product_id):
    """Adds a product to the cart or increases its quantity."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

'''@csrf_exempt
def add_to_cart_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            product = Product.objects.get(id=product_id)

            cart = request.session.get('cart', {})

            if product_id in cart:
                cart[product_id]['quantity'] += 1
            else:
                cart[product_id] = {
                    'name': product.name,
                    'price': float(product.price), 
                    'quantity': 1
                }

            request.session['cart'] = cart
            request.session.modified = True 

            return JsonResponse({'success': True, 'cart': cart})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)'''

@login_required
def remove_from_cart(request, product_id):
    """Removes a product from the cart."""
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        cart_item.delete()

    return redirect('cart')


@login_required
def update_cart(request, product_id):
    """Updates the quantity of a product in the cart."""
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = get_or_create_cart(request)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if cart_item:
            cart_item.quantity = max(1, quantity)
            cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    """Displays the cart with all items."""
    cart = get_or_create_cart(request)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def checkout(request):
    """Handles checkout logic."""
    cart = get_or_create_cart(request)

    if cart.cart_items.exists():
        cart.cart_items.all().delete()
        return render(request, 'checkout_success.html')

    return render(request, 'checkout.html', {'cart': cart})


def login_view(request):
    """Handles user login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'shop'))
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def logout_view(request):
    """Logs the user out."""
    logout(request)
    return redirect("shop")

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if not username:
            messages.error(request, "Username is required.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if not re.match(password_pattern, password):
            messages.error(request, "Password must have at least 8 characters, 1 uppercase, 1 lowercase, 1 digit, and 1 special character.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')

'''def register_view(request):
    """Registers a new user."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        
        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect("shop")

    return render(request, "register.html")
'''
def forget_password(request):
    """Handles password reset."""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email address not found.")
            return redirect("forget_password")
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_url = f"{get_current_site(request).domain}/reset_password/{uid}/{token}/"

        subject = "Password Reset Request"
        message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
        send_mail(subject, message, 'noreply@faithfashion.com', [email])

        messages.success(request, "Password reset link has been sent to your email.")
        return redirect("login")
    
    return render(request, "forget_password.html")
