from django.urls import path

from provider.views import get_goods_by_provider

urlpatterns = [
    path('get_goods_by_provider/', get_goods_by_provider, name='get_goods_by_provider'),


]