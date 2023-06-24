from django.urls import path

from orders.views import checkout
from .views import add_to_cart, cart_view, remove_from_cart, update_cart_item, order_confirmation

urlpatterns = [
    path('add_to_cart/<int:good_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),

    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),

]