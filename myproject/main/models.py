from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, related_name="restaurants", blank=True)
    location = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    delivery_time = models.PositiveIntegerField(help_text="Estimated delivery time in minutes", null=True, blank=True)
    average_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # new field for a restaurant-specific image
    image = models.ImageField(upload_to="restaurant_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="food_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="food_images/", null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Order Placed"),
        ("preparing", "Preparing"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("online", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    REFUND_STATUS_CHOICES = [
        ("no_request", "No Refund Request"),
        ("requested", "Refund Requested"),
        ("approved", "Refund Approved"),
        ("rejected", "Refund Rejected"),
        ("completed", "Refund Completed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="cod")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default="no_request")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"


class RefundRequest(models.Model):
    REFUND_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    ]

    REFUND_REASON_CHOICES = [
        ("wrong_order", "Wrong Order Received"),
        ("damaged", "Food Damaged/Not Fresh"),
        ("late_delivery", "Late Delivery"),
        ("quality_issue", "Quality Issue"),
        ("other", "Other Reason"),
    ]

    order = models.OneToOneField(Order, related_name="refund_request", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="refund_requests", on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REFUND_REASON_CHOICES)
    description = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund Request for Order {self.order.pk} - {self.status}"