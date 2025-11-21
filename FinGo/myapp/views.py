from datetime import timedelta
from decimal import Decimal, InvalidOperation
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Favorite, Notification, Order, Product, Transaction, UserProfile
from .forms import ProfileUpdateForm, RegisterForm, productForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import authenticate, login

def create_admin(request):
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Superuser already exists.")

    # Create superuser
    User.objects.create_superuser(
        username='admin',        # change as needed
        email='falloreryan649@gmail.com',  # change as needed
        password='computerscience123'    # change as needed
    )
    return HttpResponse("Superuser created successfully!")

# ✅ Utility: check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser


# ===========================
# 🌍 PUBLIC / AUTH VIEWS
# ===========================
def view_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def view_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


   # if request.user.is_authenticated:
    #     return redirect('index')

def user_logout(request):
    logout(request)
    return redirect('login')


# ===========================
# 🏠 MAIN WEBSITE PAGES
# ===========================


def view_index(request):
    return render(request, 'index.html')


@login_required
def about_website(request):
    return render(request, 'about.html')


def services_website(request):
    return render(request, 'services.html')


@login_required
def contact(request):
    return render(request, 'contact.html')


@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    results = Product.objects.filter(productName__icontains=query) if query else []

    if results.count() == 1:
        product = results.first()
        return redirect('product_detail', product_id=product.id)

    return render(request, 'search_results.html', {'results': results, 'query': query})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# ===========================
# 🧾 USER DASHBOARD & ORDERS
# ===========================

@login_required
def user_dashboard(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        try:
            quantity = Decimal(request.POST.get("quantity", "1"))
        except InvalidOperation:
            quantity = Decimal("1")

        if quantity <= 0:
            messages.error(request, "Quantity must be at least 0.25 kg.")
            return redirect('product_detail', product_id=product.id)

        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} kg available.")
            return redirect('product_detail', product_id=product.id)

        payment_method = "COD"
        total_price = product.price * quantity

        # --------------------------------------------
        # 🔥 MERGE SAME PRODUCT ORDERS, SEPARATE OTHERS
        # --------------------------------------------
        existing_order = Order.objects.filter(
            user=request.user,
            product=product,
            status="Pending"         # optional: combine only pending orders
        ).first()

        if existing_order:
            # Combine quantities + price
            existing_order.quantity += quantity
            existing_order.total_price += total_price
            existing_order.save()
            order = existing_order
        else:
            # Create new order for different product
            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_price=total_price,
            )

        # Deduct stock
        product.stock -= quantity
        product.save()

        # Remove from cart
        cart_item = CartItem.objects.filter(cart__user=request.user, product=product).first()
        if cart_item:
            cart_item.delete()

        # Create transaction
        Transaction.objects.create(
            user=request.user,
            order=order,
            amount=total_price,
            payment_method=payment_method,
            status="Pending"
        )

        # --------------------------------------------
        # 🔥 NOTIFICATIONS (Correctly inside POST)
        # --------------------------------------------
        Notification.objects.create(
            user=request.user,
            message=f"You placed an order for {quantity} kg of {product.productName}.",
            url=reverse('my_orders'),
            notif_type='order'
        )

        try:
            admin_url = reverse("admin:myapp_order_change", args=[order.id])
        except:
            admin_url = None

        Notification.objects.create(
            message=f"New order: {request.user.username} ordered {quantity} kg of {product.productName}.",
            url=admin_url,
            notif_type='order'
        )

        messages.success(request, "Order placed successfully!")
        return redirect('my_orders')

    return redirect('product_detail', product_id=product.id)


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).exclude(status__in=["Completed", "Cancelled"])
    
    total_kilos = sum(order.quantity for order in orders)
    total_price = sum(order.total_price for order in orders)

    return render(request, "my_orders.html", {
        "orders": orders,
        "total_kilos": total_kilos,
        "total_price": total_price,
    })


@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_notifications.html', {'notifications': notifications})

# ===========================
# 👤 PROFILE
# ===========================

@login_required
def profile_view(request):
    profile = request.user.userprofile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "profile.html", {"form": form})


@login_required
def update_profile(request):
    profile = request.user.userprofile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, "update_profile.html", {"form": form})


# ===========================
# 🐟 PRODUCT CRUD (USER)
# ===========================

@login_required
def view_create_product(request):
    if request.method == "POST":
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = productForm()
    return render(request, 'create_product.html', {'form': form})


@login_required
def view_products(request):
   

    query = request.GET.get('q', '')
    show_all = request.GET.get('show_all')

    if query:
        products = Product.objects.filter(
            Q(productName__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    if not show_all:
        products = products[:5]

    return render(request, 'view_product.html', {
        'products': products,
        'query': query,
        'show_all': show_all
    })


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = productForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('view_products')
    return render(request, 'delete_product.html', {'product': product})



@login_required
def my_completed_orders(request):
    completed = Order.objects.filter(user=request.user, status="Completed").order_by('-created_at')
    return render(request, 'my_completed_orders.html', {'completed_orders': completed})


@login_required
def order_history(request):
    # Get all orders of this user with status "Completed"
    completed_orders = Order.objects.filter(user=request.user, status='Completed').order_by('-created_at')
    
    context = {
        'completed_orders': completed_orders
    }
    return render(request, 'order_history.html', context)



@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Users can cancel their own orders; admins can cancel any
    if request.user != order.user and not request.user.is_staff:
        messages.error(request, "You are not allowed to cancel this order.")
        return redirect('user_order_list')  # Replace with your actual user order list URL name

    # Only allow cancelling if not already completed or cancelled
    if order.status in ['Completed', 'Cancelled']:
        messages.info(request, f"This order cannot be cancelled. Current status: {order.status}")
    else:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, "Order has been cancelled successfully.")

    # Redirect depending on user type
    if request.user.is_staff:
        return redirect('admin_order_list')  # Replace with your admin order list URL name
    else:
        return redirect('my_orders')
    


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('favorites_list')


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('favorites_list')


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites_list.html', {'favorites': favorites})



from .models import Product, CartItem, SaveForLater
from .utils import get_cart

@login_required
def cart_view(request):
    cart = get_cart(request)
    items = cart.items.all()
    saved_products = SaveForLater.objects.filter(user=request.user) if request.user.is_authenticated else []

    total = sum(item.subtotal() for item in items)

    return render(request, "cart_list.html", {
        "items": items,
        "saved_products": saved_products,
        "total": total,
    })

@login_required
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()

    return redirect("cart")

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    new_qty = int(request.POST.get("quantity"))

    if new_qty < 1:
        item.delete()
    else:
        item.quantity = new_qty
        item.save()

    return redirect("cart")

@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart")


# def save_for_later(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id)

#     if request.user.is_authenticated:
#         SaveForLater.objects.get_or_create(user=request.user, product=item.product)

#     item.delete()
#     return redirect("cart")


def move_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # Add back to cart
    CartItem.objects.get_or_create(cart=cart, product=product)

    # Remove from saved list
    SaveForLater.objects.filter(user=request.user, product=product).delete()

    return redirect("cart")

@login_required
def update_cart_quantity(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id)
        try:
            quantity = Decimal(request.POST.get('quantity', '1'))
        except InvalidOperation:
            quantity = Decimal('1')

        if quantity > 0:
            # optional: limit quantity to available stock
            if quantity > item.product.stock:
                quantity = item.product.stock
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('user_dashboard')


# ===========================
# 🧰 ADMIN DASHBOARD & MANAGEMENT
# ===========================

@staff_member_required
def admin_dashboard(request):
    # Basic stats
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    recent_orders = Order.objects.select_related('user', 'product').order_by('-id')[:5]

    # Total Income (Completed Orders Only)
    total_income = Order.objects.filter(status='Completed').aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # Top-Selling Products
    top_products = (
        Order.objects.filter(status='Completed')
        .values('product__id', 'product__productName')
        .annotate(
            total_quantity_sold=Sum('quantity'),
            total_revenue=Sum('total_price')
        )
        .order_by('-total_quantity_sold')[:5]
    )

    return render(request, 'admin_dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'total_income': total_income,
        'top_products': top_products,
    })

@staff_member_required
def admin_notifications(request):
    # Admin notifications are those where `user` is null
    notifications = Notification.objects.filter(user__isnull=True).order_by('-created_at')
    return render(request, 'admin_notifications.html', {'notifications': notifications})

@staff_member_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'manage_products.html', {'products': products})


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = productForm()
    return render(request, 'add_product.html', {'form': form})


@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = productForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'delete_product.html', {'product': product})


@staff_member_required
def manage_orders(request):
    orders = Order.objects.select_related('user').all()
    return render(request, 'manage_orders.html', {'orders': orders})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get('status')
        order.save()
        return redirect('manage_orders')
    return render(request, 'admin/update_order_status.html', {'order': order})


@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('manage_orders')
    return render(request, 'admin/confirm_delete_order.html', {'order': order})


@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


@staff_member_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, "User added successfully!")
        return redirect('manage_users')
    return render(request, 'add_user.html')


@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('manage_users')
    return render(request, 'edit_user.html', {'user': user})


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('manage_users')

@staff_member_required
def Completed_orders(request):
    completed = Order.objects.filter(status="Completed").order_by('-created_at')
    return render(request, 'completed_orders.html', {'completed_orders': completed})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_order_detail.html', {'order': order})