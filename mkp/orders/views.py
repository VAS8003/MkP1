from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from goods.all_navi import menu_user, navi_profile
from .forms import OrderForm
from .models import Order, Cart, Address, PaymentMethod, OrderItem, Status


def checkout(request):
    user = request.user
    cart = Cart.objects.get(user=user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                address_text = form.cleaned_data['address']
                payment_method = form.cleaned_data['payment_method']

                address = Address.objects.create(user=user, address=address_text)

                with transaction.atomic():
                    default_status = Status.objects.get(id=1)  # Или выберите другой ID для статуса по умолчанию
                    order = Order.objects.create(user=user, address=address, payment_method=payment_method,
                                                 status=default_status)

                    # Создание объектов OrderItem с сохранением цен на момент покупки
                    cart_items = cart.get_cart_items()
                    for cart_item in cart_items:
                        good = cart_item.good
                        quantity = cart_item.quantity
                        price = good.price_opt  # Цена товара на момент покупки
                        missing_items = []
                        for cart_item in cart_items:
                            if cart_item.quantity > cart_item.good.opt_stock:
                                missing_items.append(cart_item.good.title)
                        # Проверка доступного количества товаров
                        if quantity > good.opt_stock:
                            raise ValueError(f"Недостатня кількість товару: {', '.join(missing_items)}. В наявності: {cart_item.good.opt_stock}шт. Перейдіть в кошик і змініть кількість")

                        # Создание объекта OrderItem
                        OrderItem.objects.create(order=order, good=good, quantity=quantity, price=price)

                        # Уменьшение количества товаров в модели Good
                        good.opt_stock -= quantity
                        good.save()

                    cart.clear_cart()
                messages.success(request, '')
                return redirect('order_confirmation')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart,
        'menu': menu_user,
        'navi_profile': navi_profile,

    }

    return render(request, 'baskets/checkout.html', context)
