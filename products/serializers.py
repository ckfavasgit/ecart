from rest_framework import serializers
from .models import Product
from authentication.lang import MessageEnum

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']

    def validate(self, data):
        # Example: you can add custom validation here if needed
        return data
