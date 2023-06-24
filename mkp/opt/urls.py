from django.contrib.auth.decorators import login_required
from django.urls import path

from goods.views import LoginUser
from .views import *

urlpatterns = [
    path('seller/', login_required(seller), name='seller'),
    path('home/', login_required(index), name='home'),
    path('', LoginUser.as_view(), name='login'),
    path('my_goods/',MyGoodsList.as_view(), name='my_goods'),
    path('my_orders/',login_required(my_orders), name='my_orders'),
    path('my_buyers/',login_required(my_buyers), name='my_buyers'),
    path('goods/<int:pk>/edit/', EditGood.as_view(), name='edit_good'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('print_order/<int:order_id>/', print_order, name='print_order'),
]