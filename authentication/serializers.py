from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError({'username': 'Username is required.'})
        if not data.get('password'):
            raise serializers.ValidationError({'password': 'Password is required.'})
        return data

class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)

    def validate(self, data):
        token = data.get('token')
        request = self.context.get('request')
        if not token:
            auth_header = request.headers.get('Authorization') if request else None
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                data['token'] = token
        if not token:
            raise serializers.ValidationError({'token': 'No token provided.'})
        return data
