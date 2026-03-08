from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [


    path('register/', views.register_view, name='register'),  # <-- yaha
    path('profile/', views.profile_view, name='profile'),  # ✅ yaha sahi naam
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/track/', views.order_tracking, name='order_tracking'),
    path('order/<int:pk>/refund/', views.request_refund, name='request_refund'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
    # auth views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    # admin panel
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-restaurants/', views.manage_restaurants, name='manage_restaurants'),
    path('manage-restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('manage-restaurants/<int:pk>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('manage-restaurants/<int:pk>/delete/', views.delete_restaurant, name='delete_restaurant'),
    path('manage-food-items/', views.manage_food_items, name='manage_food_items'),
    path('manage-food-items/add/', views.add_food_item, name='add_food_item'),
    path('manage-food-items/<int:pk>/edit/', views.edit_food_item, name='edit_food_item'),
    path('manage-food-items/<int:pk>/delete/', views.delete_food_item, name='delete_food_item'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('manage-orders/<int:pk>/status/', views.update_order_status, name='update_order_status'),
]
