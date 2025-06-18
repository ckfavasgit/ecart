from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartListSerializer, AddToCartSerializer
from .service import get_cart_for_user, add_to_cart, increment_cart, decrement_cart, remove_cart
from authentication.service import api_response
from authentication.lang import MessageEnum

class CartListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart_items = get_cart_for_user(request.user)
        serializer = CartListSerializer(cart_items, many=True)
        return Response(api_response(True, 200, MessageEnum.CART_LIST_SUCCESS.value, None, serializer.data), status=200)

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart_item = add_to_cart(request.user, data['product'], data['quantity'])
        return Response(api_response(True, 200, MessageEnum.ADD_TO_CART_SUCCESS.value, None, CartListSerializer(cart_item).data), status=200)

class IncrementCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            cart_item = increment_cart(request.user, pk)
            return Response(api_response(True, 200, MessageEnum.INCREMENT_CART_SUCCESS.value, None, CartListSerializer(cart_item).data), status=200)
        except Exception as e:
            return Response(api_response(False, 400, MessageEnum.INSUFFICIENT_STOCK.value, str(e), None), status=400)

class DecrementCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            cart_item = decrement_cart(request.user, pk)
            return Response(api_response(True, 200, MessageEnum.DECREMENT_CART_SUCCESS.value, None, CartListSerializer(cart_item).data), status=200)
        except Exception as e:
            return Response(api_response(False, 400, MessageEnum.DECREMENT_CART_FAILED.value, str(e), None), status=400)

class RemoveCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        cart_item = get_cart_for_user(request.user).filter(id=pk).first()
        if not cart_item:
            return Response(api_response(False, 404, MessageEnum.CART_NOT_FOUND.value, None, None), status=404)
        remove_cart(request.user, pk)
        return Response(api_response(True, 200, MessageEnum.REMOVE_CART_SUCCESS.value, None, None), status=200)
