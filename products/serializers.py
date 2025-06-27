from rest_framework import serializers
from .models import Product
from authentication.lang import MessageEnum

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image', 'stock_quantity']

class ProductDetailSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.IntegerField(min_value=0, error_messages={
        'min_value': 'Stock quantity must be zero or positive.'
    })
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image', 'stock_quantity']

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock quantity must be zero or positive.')
        return value
