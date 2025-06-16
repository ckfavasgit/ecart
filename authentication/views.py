from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, LogoutSerializer
from .service import get_token_for_user, revoke_token, api_response
from .lang import MessageEnum

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = get_token_for_user(data['username'], data['password'], request)
        if response.status_code == 200:
            return Response(api_response(True, 200, MessageEnum.LOGIN_SUCCESS.value, None, response.json()), status=200)
        return Response(api_response(False, response.status_code, MessageEnum.LOGIN_FAILED.value, response.json(), None), status=response.status_code)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = revoke_token(data['token'], request)
        if response.status_code == 200:
            try:
                resp_json = response.json()
            except Exception:
                resp_json = None
            if resp_json and resp_json.get('error'):
                return Response(api_response(False, 400, MessageEnum.LOGOUT_FAILED.value, resp_json, None), status=400)
            return Response(api_response(True, 200, MessageEnum.LOGOUT_SUCCESS.value, None, None), status=200)
        return Response(api_response(False, response.status_code, MessageEnum.LOGOUT_FAILED.value, response.json(), None), status=response.status_code)
