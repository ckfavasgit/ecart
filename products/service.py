from .models import Product
from django.shortcuts import get_object_or_404

def get_all_products():
    return Product.objects.all()

def get_product_by_id(product_id):
    return get_object_or_404(Product, id=product_id)
