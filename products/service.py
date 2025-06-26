from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Q

def get_all_products(keyword=None):
    if keyword:
        return Product.objects.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )
    return Product.objects.all()

def get_product_by_id(product_id):
    return get_object_or_404(Product, id=product_id)
