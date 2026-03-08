from django import forms
from .models import Restaurant, FoodItem, Order


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'rating', 'delivery_time', 'average_price', 'categories']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['restaurant', 'name', 'description', 'price', 'available', 'image']


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
