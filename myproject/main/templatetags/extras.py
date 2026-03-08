from django import template
from main.models import FoodItem

register = template.Library()

@register.filter
def get_item(food_items, key):
    try:
        return FoodItem.objects.get(pk=int(key))
    except (FoodItem.DoesNotExist, ValueError):
        return None
