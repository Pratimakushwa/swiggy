from django.contrib import admin
from .models import Category, Restaurant, FoodItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "rating", "delivery_time", "image")
    fields = ("name", "location", "rating", "delivery_time", "average_price", "image")
    search_fields = ("name",)
    inlines = [FoodItemInline]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "available")
    list_filter = ("available", "restaurant")
    search_fields = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("price",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "status", "total_price", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("user__username", "restaurant__name")
    inlines = [OrderItemInline]
