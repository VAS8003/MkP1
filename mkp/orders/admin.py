from django.contrib import admin

from orders.models import Order, Address, PaymentMethod, OrderItem, Status

# Register your models here.
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(PaymentMethod)
admin.site.register(OrderItem)
admin.site.register(Status)

