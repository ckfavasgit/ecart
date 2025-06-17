from django.urls import path
from .views import CartListAPIView, AddToCartAPIView, EditCartAPIView, RemoveCartAPIView

urlpatterns = [
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('add', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('edit/<int:pk>', EditCartAPIView.as_view(), name='edit-cart'),
    path('remove/<int:pk>', RemoveCartAPIView.as_view(), name='remove-cart'),
]
