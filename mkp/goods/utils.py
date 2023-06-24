from django.db.models import Count
from django.core.cache import cache

from .all_navi import menu_seller, menu_user
from .models import *

import requests
from django.conf import settings



class DataMixin:
    paginate_by = 15

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('good'))
        brands = Brand.objects.annotate(Count('good'))
        context['menu_seller'] = menu_seller
        context['menu_user'] = menu_user
        context['cats'] = cats
        context['brands'] = brands
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'brand_selected' not in context:
            context['brand_selected'] = 0

        # Отримати корзину користувача
        user = self.request.user
        if user.is_authenticated:
            cart = user.cart
            cart_items = cart.get_cart_items()
            total_quantity = sum(item.quantity for item in cart_items)
            total_price = cart.get_total_price()
            context['cart_items'] = cart_items
            context['total_quantity'] = total_quantity
            context['total_price'] = total_price

        return context




def send_order_notification(last_order):
    user = last_order.user
    message = f"Отримано нове замовлення з ідентифікатором {last_order} - {user.first_name}"
    chat_id = settings.TELEGRAM_CHAT_ID

    response = requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": message}
    )

    if response.status_code != 200:
        print("Помилка при відправці повідомлення в Telegram.")

