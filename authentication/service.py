from django.conf import settings
from rest_framework.response import Response
import requests


def get_token_for_user(username, password, request):
    token_url = request.build_absolute_uri('/o/token/')
    client_id = settings.OAUTH2_CLIENT_ID
    client_secret = settings.OAUTH2_CLIENT_SECRET
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(token_url, data=payload)
    return response

def revoke_token(token, request):
    revoke_url = request.build_absolute_uri('/o/revoke_token/')
    client_id = settings.OAUTH2_CLIENT_ID
    client_secret = settings.OAUTH2_CLIENT_SECRET
    payload = {
        'token': token,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(revoke_url, data=payload)
    return response

def api_response(status_bool, status_code, message, error=None, data=None):
    return {
        'status': status_bool,
        'statusCode': status_code,
        'message': message,
        'error': error,
        'data': data
    }
