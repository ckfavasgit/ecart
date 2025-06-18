from django.urls import path
from .views import CartListAPIView, AddToCartAPIView, IncrementCartAPIView, DecrementCartAPIView, RemoveCartAPIView

urlpatterns = [
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('add', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('increment/<int:pk>', IncrementCartAPIView.as_view(), name='increment-cart'),
    path('decrement/<int:pk>', DecrementCartAPIView.as_view(), name='decrement-cart'),
    path('remove/<int:pk>', RemoveCartAPIView.as_view(), name='remove-cart'),
]
