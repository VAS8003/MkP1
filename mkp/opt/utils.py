from django.db.models import Count
from django.core.cache import cache

from goods.all_navi import menu_seller, navi_seller
from goods.models import Category
from .models import *

class DataSellerMixin:
    paginate_by = 15
    def get_user_context(self, **kwargs):
        context = kwargs

        cats = Category.objects.annotate(Count('good'))

        context['menu'] = menu_seller
        context['navi_seller'] = navi_seller
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context