from rest_framework import serializers
from .models import Cart
from products.models import Product
from authentication.lang import MessageEnum
from rest_framework.exceptions import ValidationError as DRFValidationError

class CartListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity']

class AddToCartSerializer(serializers.Serializer):
    product = serializers.IntegerField(
        error_messages={
            'required': MessageEnum.PRODUCT_REQUIRED.value
        }
    )
    quantity = serializers.IntegerField(min_value=1,
        error_messages={
            'required': MessageEnum.QUANTITY_REQUIRED.value,
            'min_value': MessageEnum.QUANTITY_MIN_VALUE.value
        }
    )

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except DRFValidationError as exc:
            from authentication.service import api_response
            response = api_response(
                False,
                400,
                MessageEnum.ADD_TO_CART_FAILED.value,
                exc.detail,
                None
            )
            raise DRFValidationError(response)

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product': MessageEnum.PRODUCT_NOT_FOUND.value})
        if data['quantity'] > product.stock_quantity:
            raise serializers.ValidationError({'quantity': MessageEnum.INSUFFICIENT_STOCK.value})
        return data

class EditCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1,
        error_messages={
            'required': MessageEnum.QUANTITY_REQUIRED.value,
            'min_value': MessageEnum.QUANTITY_MIN_VALUE.value
        }
    )

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except DRFValidationError as exc:
            from authentication.service import api_response
            response = api_response(
                False,
                400,
                MessageEnum.EDIT_CART_FAILED.value,
                exc.detail,
                None
            )
            raise DRFValidationError(response)

    def validate_quantity(self, value):
        cart = self.context.get('cart')
        if cart and value > cart.product.stock_quantity:
            raise serializers.ValidationError(MessageEnum.INSUFFICIENT_STOCK.value)
        return value
