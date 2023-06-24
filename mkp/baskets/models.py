from django.db import models
from django.conf import settings

from goods.models import Good
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    goods = models.ManyToManyField(Good, through='CartItem')

    def add_to_cart(self, good, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=self, good=good)
        cart_item.quantity += quantity
        cart_item.save()

    def remove_from_cart(self, good):
        CartItem.objects.filter(cart=self, good=good).delete()

    def clear_cart(self):
        CartItem.objects.filter(cart=self).delete()

    def get_cart_items(self):
        return CartItem.objects.filter(cart=self)

    def get_total_price(self):
        cart_items = self.get_cart_items()
        total_price = sum(cart_item.get_total_price() for cart_item in cart_items)
        return total_price

    def get_total_quantity(self):
        cart_items = self.get_cart_items()
        total_quantity = sum(cart_item.quantity for cart_item in cart_items)
        return total_quantity


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.good.price_opt * self.quantity
