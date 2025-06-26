from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProductListSerializer, ProductDetailSerializer
from .service import get_all_products, get_product_by_id
from authentication.service import api_response
from authentication.lang import MessageEnum

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        keyword = request.query_params.get('keyword')
        products = get_all_products(keyword=keyword)
        serializer = ProductListSerializer(products, many=True)
        return Response(api_response(True, 200, MessageEnum.PRODUCT_LIST_SUCCESS.value, None, serializer.data), status=200)

class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            product = get_product_by_id(pk)
            serializer = ProductDetailSerializer(product)
            return Response(api_response(True, 200, MessageEnum.PRODUCT_DETAIL_SUCCESS.value, None, serializer.data), status=200)
        except Exception as e:
            return Response(api_response(False, 404, MessageEnum.PRODUCT_NOT_FOUND.value, str(e), None), status=404)
