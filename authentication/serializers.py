from rest_framework import serializers
from .lang import MessageEnum
from rest_framework.exceptions import ValidationError as DRFValidationError

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        error_messages={
            'required': MessageEnum.USERNAME_REQUIRED.value,
            'blank': MessageEnum.USERNAME_REQUIRED.value
        }
    )
    password = serializers.CharField(
        error_messages={
            'required': MessageEnum.PASSWORD_REQUIRED.value,
            'blank': MessageEnum.PASSWORD_REQUIRED.value
        }
    )

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except DRFValidationError as exc:
            from .service import api_response
            response = api_response(
                False,
                400,
                MessageEnum.LOGIN_FAILED.value,
                exc.detail,
                None
            )
            raise DRFValidationError(response)

    def validate(self, data):
        return data

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except DRFValidationError as exc:
            from .service import api_response
            response = api_response(
                False,
                400,
                MessageEnum.LOGOUT_FAILED.value,
                exc.detail,
                None
            )
            raise DRFValidationError(response)

    def validate(self, data):
        token = data.get('token')
        request = self.context.get('request')
        if not token:
            auth_header = request.headers.get('Authorization') if request else None
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                data['token'] = token
        if not token:
            raise serializers.ValidationError({'token': MessageEnum.TOKEN_REQUIRED.value})
        return data
