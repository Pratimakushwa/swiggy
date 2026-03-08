import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from main.models import Restaurant, FoodItem, Category

# Create categories
categories = [
    {"name": "North Indian", "slug": "north-indian"},
    {"name": "South Indian", "slug": "south-indian"},
    {"name": "Pizza", "slug": "pizza"},
    {"name": "Burger", "slug": "burger"},
    {"name": "Desserts", "slug": "desserts"},
    {"name": "Ice Cream", "slug": "ice-cream"},
    {"name": "Dosa", "slug": "dosa"},
    {"name": "Rolls", "slug": "rolls"},
    {"name": "Shake", "slug": "shake"},
    {"name": "Coffee", "slug": "coffee"},
    {"name": "Chole Bhature", "slug": "chole-bhature"},
    {"name": "Vada", "slug": "vada"},
    {"name": "Biryani", "slug": "biryani"},
    {"name": "Cake", "slug": "cake"},
]

cat_dict = {}
for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={"slug": cat_data["slug"]}
    )
    cat_dict[cat_data["slug"]] = cat
    if created:
        print(f"Created category: {cat.name}")

# Create restaurants
# each record may now include an optional image url (already hosted or local)
restaurants_data = [
    {
        "name": "DEUCE",
        "location": "Nipania, Indore",
        "rating": 4.8,
        "delivery_time": 10.4,
        "categories": ["north-indian"],
        "image_url": "https://example.com/images/deuce.jpg",
    },
    {
        "name": "Kabelo Veg Barbecue",
        "location": "Rau, Indore",
        "rating": 4.9,
        "delivery_time": 8.4,
        "categories": ["north-indian"],
        "image_url": "https://example.com/images/kabelo.jpg",
    },
    {
        "name": "Haldiram's Sweets and...",
        "location": "High Street Apollo, Bypass South, Indore",
        "rating": 4.9,
        "delivery_time": 10.2,
        "categories": ["north-indian"],
        "image_url": "https://example.com/images/haldiram.jpg",
    },
    {
        "name": "Pizza Palace",
        "location": "Downtown Indore",
        "rating": 4.5,
        "delivery_time": 30,
        "categories": ["pizza"],
        "image_url": "https://example.com/images/pizza_palace.jpg",
    },
    {
        "name": "Burger Barn",
        "location": "Central Indore",
        "rating": 4.2,
        "delivery_time": 25,
        "categories": ["burger"],
        "image_url": "https://example.com/images/burger_barn.jpg",
    },
    {
        "name": "Biryani House",
        "location": "Old City, Indore",
        "rating": 4.6,
        "delivery_time": 35,
        "categories": ["biryani"],
        "image_url": "https://example.com/images/biryani_house.jpg",
    },
    {
        "name": "South Indian Delights",
        "location": "MG Road, Indore",
        "rating": 4.4,
        "delivery_time": 20,
        "categories": ["south-indian", "dosa"],
        "image_url": "https://example.com/images/south_indian.jpg",
    },
    {
        "name": "Sweet Dreams Bakery",
        "location": "Rajwada, Indore",
        "rating": 4.7,
        "delivery_time": 15,
        "categories": ["desserts", "cake"],
        "image_url": "https://example.com/images/sweet_dreams.jpg",
    },
]

for rest_data in restaurants_data:
    rest, created = Restaurant.objects.get_or_create(
        name=rest_data["name"],
        location=rest_data["location"],
        defaults={
            "rating": rest_data["rating"],
            "delivery_time": rest_data["delivery_time"],
            "average_price": 300.00,
        }
    )
    for cat_slug in rest_data["categories"]:
        if cat_slug in cat_dict:
            rest.categories.add(cat_dict[cat_slug])
    # if an image URL is provided, fetch it and save to the ImageField
    image_url = rest_data.get("image_url")
    if image_url and not rest.image:
        try:
            from django.core.files import File
            import requests
            resp = requests.get(image_url, stream=True)
            if resp.status_code == 200:
                filename = os.path.basename(image_url)
                rest.image.save(filename, File(resp.raw), save=True)
        except Exception as e:
            print(f"Failed to download image for {rest.name}: {e}")
    if created:
        print(f"Created restaurant: {rest.name}")

# Create food items
food_items = [
    {"name": "Margherita Pizza", "restaurant": "Pizza Palace", "description": "Classic cheese pizza", "price": 299.00},
    {"name": "Pepperoni Pizza", "restaurant": "Pizza Palace", "description": "Pepperoni & cheese", "price": 349.00},
    {"name": "Classic Burger", "restaurant": "Burger Barn", "description": "Beef patty with lettuce & tomato", "price": 159.00},
    {"name": "Cheese Burger", "restaurant": "Burger Barn", "description": "Beef patty with melted cheese", "price": 179.00},
    {"name": "Biryani", "restaurant": "Biryani House", "description": "Traditional Hyderabadi biryani", "price": 349.00},
    {"name": "Chicken Biryani", "restaurant": "Biryani House", "description": "Spiced chicken biryani", "price": 379.00},
    {"name": "Masala Dosa", "restaurant": "South Indian Delights", "description": "Crispy dosa with sambar", "price": 199.00},
    {"name": "Idli", "restaurant": "South Indian Delights", "description": "Steamed rice cakes", "price": 99.00},
    {"name": "Chocolate Cake", "restaurant": "Sweet Dreams Bakery", "description": "Rich chocolate cake", "price": 289.00},
    {"name": "Cheesecake", "restaurant": "Sweet Dreams Bakery", "description": "Classic New York cheesecake", "price": 249.00},
]

for item_data in food_items:
    try:
        restaurant = Restaurant.objects.get(name=item_data["restaurant"])
        food, created = FoodItem.objects.get_or_create(
            restaurant=restaurant,
            name=item_data["name"],
            defaults={
                "description": item_data["description"],
                "price": item_data["price"],
                "available": True,
            }
        )
        if created:
            print(f"Created food item: {food.name} at {restaurant.name}")
    except Restaurant.DoesNotExist:
        print(f"Restaurant {item_data['restaurant']} not found")

print("\n✅ Seed data created successfully!")
print("\nYou can also add more data via Django Admin at /admin/")

