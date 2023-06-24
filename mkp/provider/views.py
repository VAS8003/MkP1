from django.contrib.auth.decorators import login_required
from goods.all_navi import menu_user, navi_provider
from django.shortcuts import render
from goods.models import Good

@login_required
def get_goods_by_provider(request):
    user = request.user  # Предполагается, что пользователь аутентифицирован
    goods = Good.objects.filter(provider=user)

    # Вычисляем разницу между full_stock и opt_stock для каждого товара
    goods_with_difference = []
    for good in goods:
        difference = good.full_stock - good.opt_stock
        goods_with_difference.append((good, difference))

    context = {
        'title': 'Наявність моїх товарів',
        'menu': menu_user,
        'goods_with_difference': goods_with_difference,
        'navi_provider': navi_provider,
    }
    return render(request, 'provider/get_goods_by_provider.html', context)