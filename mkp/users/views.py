from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404
from goods.all_navi import menu_user, navi_provider, navi_profile
from orders.models import Order, OrderItem


def profile(request):
    user = request.user
    cart = user.cart
    cart_items = cart.get_cart_items()
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = cart.get_total_price()

    context = {
        'menu': menu_user,
        'title': 'Профіль користувача',
        'navi_profile': navi_profile,
        'navi_provider': navi_provider,
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price


    }

    return render(request, 'users/profile.html', context=context)

def user(request):
    context = {
        'menu': menu_user,
        'title': 'Профіль користувача',
        'navi_profile': navi_profile,
        'navi_provider': navi_provider,

    }

    return render(request, 'users/user.html', context=context)


@login_required
def history_orders(request):
    user = request.user
    cart = user.cart
    cart_items = cart.get_cart_items()
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = cart.get_total_price()
    orders = Order.objects.filter(user=user)



    for order in orders:
        order.total_quantity = order.items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        order.total_amount = order.items.annotate(subtotal=F('price') * F('quantity')).aggregate(total=Sum('subtotal'))['total']

    paginator = Paginator(orders, 5)  # Розмір сторінки: 10 замовлень

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu_user,
        'title': 'Історія замовлень',
        'navi_profile': navi_profile,
        'orders': page_obj,  # Використовуємо сторінку замовлень замість всього списку
        'navi_provider': navi_provider,
        'paginator': paginator,
        'page_obj': page_obj,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'users/history_orders.html', context=context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.total_quantity = order.items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    order.total_amount = order.items.annotate(subtotal=F('price') * F('quantity')).aggregate(total=Sum('subtotal'))[
            'total']
    context = {
        'menu': menu_user,
        'title': 'Профіль користувача',
        'navi_profile': navi_profile,
        'navi_provider': navi_provider,
        'order': order,

    }
    return render(request, 'users/order_detail.html', context)