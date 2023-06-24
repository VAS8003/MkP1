from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from goods.utils import send_order_notification
from orders.models import Order
from .models import Cart, CartItem
from .forms import AddToCartForm, RemoveFromCartForm
from goods.models import Good
from goods.all_navi import *

@login_required
def add_to_cart(request, good_id):
    good = Good.objects.get(pk=good_id)
    quantity = int(request.POST.get('quantity', 0))
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_to_cart(good, quantity=quantity)
    # return redirect(request, 'users/cart_view.html')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def cart_view(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)

    cart_items = cart.get_cart_items()
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = cart.get_total_price()

    if request.method == 'POST':
        add_to_cart_form = AddToCartForm(request.POST)
        remove_from_cart_form = RemoveFromCartForm(request.POST)

        # Остальной код для обработки отправки формы

    else:
        add_to_cart_form = AddToCartForm()
        remove_from_cart_form = RemoveFromCartForm()

    missing_items = []
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.good.opt_stock:
            missing_items.append(cart_item.good.title)

    if missing_items:
        message = f"Недостатня кількість товару: {', '.join(missing_items)}. "
        messages.error(request, message)

    context = {
        'cart': cart,
        'title': 'Мій кошик',
        'menu': menu_user,
        'navi_profile': navi_profile,
        'navi_provider': navi_provider,
        'cart_items': cart_items,
        'add_to_cart_form': add_to_cart_form,
        'remove_from_cart_form': remove_from_cart_form,
        'total_quantity': total_quantity,
        'total_price': total_price
    }

    return render(request, 'baskets/cart_view.html', context)


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart_view')  # Перенаправление на страницу корзины после обновления количества

    context = {
        'cart_item': cart_item,
    }
    return render(request, 'baskets/update_cart_item.html', context)

def order_confirmation(request):
    last_order = Order.objects.filter(user=request.user).order_by('-id').first()
    send_order_notification(last_order)
    context = {
        'menu': menu_user,
        'title': 'Профіль користувача',
        'navi_profile': navi_profile

    }
    return render(request, 'baskets/order_confirmation.html', context)

