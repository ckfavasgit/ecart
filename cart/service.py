from .models import Cart
from products.models import Product
from django.shortcuts import get_object_or_404

def get_cart_for_user(user):
    return Cart.objects.filter(user=user)

def add_to_cart(user, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    # Decrement stock
    product.stock_quantity -= quantity
    product.save()
    return cart_item

def edit_cart(user, cart_id, quantity):
    cart_item = get_object_or_404(Cart, id=cart_id, user=user)
    product = cart_item.product
    # Check if enough stock is available (considering current cart quantity)
    available_stock = product.stock_quantity + cart_item.quantity
    if quantity > available_stock:
        from authentication.lang import MessageEnum
        from rest_framework.exceptions import ValidationError
        raise ValidationError({'quantity': MessageEnum.INSUFFICIENT_STOCK.value})
    # Calculate the difference and update stock
    diff = quantity - cart_item.quantity
    cart_item.quantity = quantity
    cart_item.save()
    product.stock_quantity -= diff
    product.save()
    return cart_item

def remove_cart(user, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=user)
    # Restore stock when removing from cart
    product = cart_item.product
    product.stock_quantity += cart_item.quantity
    product.save()
    cart_item.delete()
    return True
