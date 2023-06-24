from django.contrib import admin
from .models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id','title','article', 'brand','cat',
    'is_published', 'owner', 'provider', 'price_opt', 'price_b2c', 'price_drop', 'price_mrc', 'opt_stock',
                    'b2c_stock', 'drop_stock')
    list_filter = ('brand','cat', 'owner')
    search_fields = ('title','article')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Good, GoodsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
