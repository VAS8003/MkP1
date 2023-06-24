from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from baskets.views import cart_view
from .views import *


urlpatterns = [
    path('profile/', profile, name='profile'),
    path('user/', user, name='user'),
    path('cart_view/', cart_view, name='cart_view'),
    path('history_orders/', history_orders, name='history_orders'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),

]