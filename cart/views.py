from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartListSerializer, AddToCartSerializer, EditCartSerializer
from .service import get_cart_for_user, add_to_cart, edit_cart, remove_cart
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

class EditCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        cart_item = get_cart_for_user(request.user).filter(id=pk).first()
        if not cart_item:
            return Response(api_response(False, 404, MessageEnum.CART_NOT_FOUND.value, None, None), status=404)
        serializer = EditCartSerializer(data=request.data, context={'cart': cart_item})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart_item = edit_cart(request.user, pk, data['quantity'])
        return Response(api_response(True, 200, MessageEnum.EDIT_CART_SUCCESS.value, None, CartListSerializer(cart_item).data), status=200)

class RemoveCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        cart_item = get_cart_for_user(request.user).filter(id=pk).first()
        if not cart_item:
            return Response(api_response(False, 404, MessageEnum.CART_NOT_FOUND.value, None, None), status=404)
        remove_cart(request.user, pk)
        return Response(api_response(True, 200, MessageEnum.REMOVE_CART_SUCCESS.value, None, None), status=200)
