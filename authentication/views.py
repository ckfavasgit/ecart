from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, LogoutSerializer
from .service import get_token_for_user, revoke_token

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = get_token_for_user(data['username'], data['password'], request)
        if response.status_code == 200:
            return Response(response.json())
        return Response(response.json(), status=response.status_code)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = revoke_token(data['token'], request)
        if response.status_code == 200:
            return Response({'detail': 'Token revoked successfully.'})
        return Response(response.json(), status=response.status_code)
