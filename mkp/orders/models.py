from django.db.models import Sum, F

from orders.models import *
from baskets.models import *
# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length=155)
    def __str__(self):
        return self.status

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_method


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_quantity(self):
        cart_items = self.items.all()
        total_quantity = sum(cart_item.quantity for cart_item in cart_items)
        return total_quantity

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара на момент покупки

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"Order #{self.order.id} - Item #{self.id}"

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"

def calculate_order_total(order):
    total_amount = order.items.aggregate(total=Sum(F('quantity') * F('price')))['total']
    return total_amount if total_amount is not None else 0

def calculate_order_quantity(order):
    total_quantity = order.items.aggregate(total=Sum('quantity'))['total']
    return total_quantity if total_quantity is not None else 0

