from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import Category, Restaurant, FoodItem, Order, OrderItem
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# ---------------- Register ----------------
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1:
            messages.error(request, "Username, email, and password are required")
            return redirect('main:register')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('main:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('main:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('main:register')

        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Account created successfully. You can now login.")
        return redirect('main:login')
    
    return render(request, 'main/register.html')


# ---------------- Login ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('main:home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('main:login')
    
    return render(request, 'main/login.html')


# ---------------- Logout ----------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('main:login')
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

# Profile view
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'main/profile.html', {'user': user})
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('main:home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:home')


def home(request):
    # show all restaurants on homepage
    restaurants = Restaurant.objects.all()
    # derive categories present in these restaurants
    categories = Category.objects.filter(restaurants__in=restaurants).distinct()
    return render(request, 'main/home.html', {'restaurants': restaurants, 'categories': categories})


def restaurant_list(request):
    qs = Restaurant.objects.all()
    query = request.GET.get('q')
    location = request.GET.get('location')
    category_slug = request.GET.get('category')
    if query:
        qs = qs.filter(name__icontains=query)
    if location:
        qs = qs.filter(location__icontains=location)
    if category_slug:
        qs = qs.filter(categories__slug=category_slug)
    return render(request, 'main/restaurant_list.html', {'restaurants': qs})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    # restaurant ke menu items
    items = FoodItem.objects.filter(restaurant=restaurant, available=True)

    # cart items
    cart = request.session.get('cart', {})
    food_ids = [int(fid) for fid in cart.keys()]

    food_items = FoodItem.objects.filter(id__in=food_ids)

    # dictionary bana rahe hain taki template me easily mil jaye
    food_items_dict = {str(food.id): food for food in food_items}

    return render(request, 'main/restaurant_detail.html', {
        'restaurant': restaurant,
        'items': items,
        'food_items': food_items_dict
    })

# simple session cart

def _get_cart(request):
    return request.session.setdefault('cart', {})


def add_to_cart(request, food_id):

    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('main:cart')


def update_cart(request):

    cart = request.session.get('cart', {})

    for key, value in request.POST.items():

        if key.startswith('qty_'):

            food_id = key.split('_')[1]
            qty = int(value)

            if qty <= 0:
                cart.pop(food_id, None)
            else:
                cart[food_id] = qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('main:cart')

def cart_view(request):

    cart = request.session.get('cart', {})

    items = []
    total = 0

    for food_id, qty in cart.items():

        food = FoodItem.objects.get(id=food_id)

        subtotal = food.price * qty
        total += subtotal

        items.append({
            'food': food,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render(request, 'main/cart.html', {
        'items': items,
        'total': total
    })
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    # User selected items from form
    selected_items = request.POST.getlist('selected_items')  # e.g. ['2', '5']
    if selected_items:
        checkout_cart = {fid: cart[fid] for fid in selected_items if fid in cart}
    else:
        checkout_cart = cart.copy()  # agar koi select nahi kiya to pura cart

    if not checkout_cart:
        messages.error(request, "No items selected for checkout.")
        return redirect('main:cart')

    # Calculate total
    items = []
    subtotal = 0
    for food_id, qty in checkout_cart.items():
        food = FoodItem.objects.get(pk=int(food_id))
        subtotal_item = food.price * qty
        items.append({'food': food, 'quantity': qty, 'subtotal': subtotal_item})
        subtotal += subtotal_item

    if request.method == 'POST' and request.POST.get('address'):
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'cod')

        first_food = FoodItem.objects.get(pk=int(next(iter(checkout_cart))))
        order = Order.objects.create(
            user=request.user,
            restaurant=first_food.restaurant,
            total_price=subtotal + 40,  # delivery charges
            address=address,
            payment_method=payment_method,
            payment_status='pending'
        )

        # Sirf selected items ka order item create karo
        for food_id, qty in checkout_cart.items():
            food = FoodItem.objects.get(pk=int(food_id))
            price = food.price * qty
            OrderItem.objects.create(order=order, food_item=food, quantity=qty, price=price)

        # Razorpay handling
        if payment_method == 'razorpay':
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(dict(
                amount=int(order.total_price * 100),
                currency='INR',
                receipt=f'order_{order.pk}',
                payment_capture='1'
            ))
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            return render(request, 'main/razorpay_payment.html', {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
            })
        else:
            messages.success(request, "Order placed successfully!")
            return redirect('main:order_tracking', pk=order.pk)

    return render(request, 'main/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'delivery_charges': 40,
        'total': subtotal + 40
    })
# @login_required
# @csrf_exempt
# @login_required
# def checkout(request):
#     cart = _get_cart(request)  # session cart

#     selected_items = request.POST.getlist('selected_items')
#     if selected_items:
#         checkout_cart = {fid: cart[fid] for fid in selected_items if fid in cart}
#     else:
#         checkout_cart = cart.copy()

#     if not checkout_cart:
#         return redirect('main:cart')

#     # Calculate total
#     items = []
#     subtotal = 0
#     for food_id, qty in checkout_cart.items():
#         food = FoodItem.objects.get(pk=int(food_id))
#         item_total = food.price * qty
#         items.append({'food': food, 'quantity': qty, 'subtotal': item_total})
#         subtotal += item_total

#     if request.method == 'POST' and request.POST.get('address'):
#         address = request.POST.get('address', '')
#         payment_method = request.POST.get('payment_method', 'cod')

#         first_food = FoodItem.objects.get(pk=int(next(iter(checkout_cart))))
#         order = Order.objects.create(
#             user=request.user,
#             restaurant=first_food.restaurant,
#             total_price=0,
#             address=address,
#             payment_method=payment_method,
#             payment_status='completed' if payment_method == 'cod' else 'pending'
#         )

#         total = 0
#         for food_id, qty in checkout_cart.items():
#             food = FoodItem.objects.get(pk=int(food_id))
#             price = food.price * qty
#             OrderItem.objects.create(order=order, food_item=food, quantity=qty, price=price)
#             total += price

#         order.total_price = total + 40
#         order.save()

#         if payment_method == 'razorpay':
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             razorpay_order = client.order.create(dict(
#                 amount=int(order.total_price * 100),
#                 currency='INR',
#                 receipt=f'order_{order.pk}',
#                 payment_capture='1'
#             ))
#             order.razorpay_order_id = razorpay_order['id']
#             order.save()

#             return render(request, 'main/razorpay_payment.html', {
#                 'order': order,
#                 'razorpay_order_id': razorpay_order['id'],
#                 'razorpay_key': settings.RAZORPAY_KEY_ID,
#             })
#         else:
#             # ✅ COD - **cart ko touch mat karo**
#             messages.success(request, 'Your order has been placed.')
#             return redirect('main:order_tracking', pk=order.pk)
#     else:
#         return render(request, 'main/checkout.html', {
#             'items': items,
#             'subtotal': subtotal,
#             'delivery_charges': 40,
#             'total': subtotal + 40
#         })
@login_required
def order_tracking(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'main/order_tracking.html', {'order': order})
@login_required
@csrf_exempt
def razorpay_callback(request):
    if request.method == 'POST':
        try:
            payment_data = json.loads(request.body)
            order_id = payment_data.get('order_id')
            razorpay_payment_id = payment_data.get('razorpay_payment_id')
            razorpay_signature = payment_data.get('razorpay_signature')

            order = get_object_or_404(Order, pk=order_id, user=request.user)

            # Razorpay signature verify
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': order.razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            order.payment_status = 'completed'
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()

            # ✅ Yaha cart ko bilkul touch nahi karna
            # User khud remove kare tab hi cart update hoga

            return JsonResponse({'status': 'success', 'message': 'Payment verified', 'order_id': order.pk})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/my_orders.html', {'orders': orders})


@login_required
def request_refund(request, pk):
    from .models import RefundRequest
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    # Check if order is eligible for refund
    if order.status != 'delivered':
        messages.error(request, 'Only delivered orders can be refunded.')
        return redirect('main:order_tracking', pk=order.pk)
    
    if order.refund_status != 'no_request':
        messages.error(request, 'A refund request already exists for this order.')
        return redirect('main:order_tracking', pk=order.pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        description = request.POST.get('description', '')
        
        if not reason or not description:
            messages.error(request, 'Please fill in all fields.')
            return redirect('main:request_refund', pk=order.pk)
        
        # Create refund request
        refund = RefundRequest.objects.create(
            order=order,
            user=request.user,
            reason=reason,
            description=description,
            refund_amount=order.total_price
        )
        
        # Update order refund status
        order.refund_status = 'requested'
        order.save()
        
        messages.success(request, 'Refund request submitted successfully. Our team will review it soon.')
        return redirect('main:order_tracking', pk=order.pk)
    
    return render(request, 'main/request_refund.html', {'order': order})


# --- admin side views ---
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import RestaurantForm, FoodItemForm, OrderStatusForm


def staff_required(view_func):
    decorated = user_passes_test(lambda u: u.is_staff, login_url='main:login')(view_func)
    return decorated


@staff_required
def admin_dashboard(request):
    User = get_user_model()
    total_users = User.objects.count()
    total_restaurants = Restaurant.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='placed').count()
    return render(request, 'main/admin/dashboard.html', {
        'total_users': total_users,
        'total_restaurants': total_restaurants,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
    })


@staff_required
def manage_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/admin/manage_restaurants.html', {'restaurants': restaurants})


@staff_required
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:manage_restaurants')
    else:
        form = RestaurantForm()
    return render(request, 'main/admin/restaurant_form.html', {'form': form})


@staff_required
def edit_restaurant(request, pk):
    rest = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=rest)
        if form.is_valid():
            form.save()
            return redirect('main:manage_restaurants')
    else:
        form = RestaurantForm(instance=rest)
    return render(request, 'main/admin/restaurant_form.html', {'form': form, 'restaurant': rest})


@staff_required
def delete_restaurant(request, pk):
    rest = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        rest.delete()
        return redirect('main:manage_restaurants')
    return render(request, 'main/admin/confirm_delete.html', {'object': rest, 'type': 'restaurant'})


@staff_required
def manage_food_items(request):
    items = FoodItem.objects.select_related('restaurant').all()
    return render(request, 'main/admin/manage_food_items.html', {'items': items})


@staff_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:manage_food_items')
    else:
        form = FoodItemForm()
    return render(request, 'main/admin/fooditem_form.html', {'form': form})


@staff_required
def edit_food_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('main:manage_food_items')
    else:
        form = FoodItemForm(instance=item)
    return render(request, 'main/admin/fooditem_form.html', {'form': form, 'item': item})


@staff_required
def delete_food_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('main:manage_food_items')
    return render(request, 'main/admin/confirm_delete.html', {'object': item, 'type': 'food item'})


@staff_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'main/admin/manage_orders.html', {'orders': orders})


@staff_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('main:manage_orders')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'main/admin/order_status_form.html', {'form': form, 'order': order})
