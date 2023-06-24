from django.contrib import admin
from .models import *

# class CartAdmin(admin.ModelAdmin):
    # list_display = ('user', 'goods')

admin.site.register(Cart)
admin.site.register(CartItem)
