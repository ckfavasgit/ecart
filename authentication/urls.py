from django.urls import path
from .views import LoginAPIView, LogoutAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='custom-login'),
    path('logout', LogoutAPIView.as_view(), name='custom-logout'),
]
