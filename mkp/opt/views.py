from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from goods.all_navi import menu_seller, navi_seller
from goods.forms import AddGoodForms
from goods.models import *
from opt.forms import OrderStatusForm
from opt.utils import  DataSellerMixin
from orders.models import Order, OrderItem, Status, calculate_order_total, calculate_order_quantity


class MyGoodsList(DataSellerMixin, LoginRequiredMixin, ListView):
    model = Good
    template_name = 'opt/show_my_goods.html'
    context_object_name = 'my_goods'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мої товари")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        return Good.objects.filter(owner=user, is_published=True).select_related('cat')

class EditGood(LoginRequiredMixin, UpdateView):
    model = Good
    form_class = AddGoodForms
    template_name = 'goods/edit_good.html'
    success_url = reverse_lazy('my_goods')


def seller(requests):
    context = {
        'title': 'Сторінка продавця',
        'menu': menu_seller,
        'navi_seller': navi_seller,
    }
    return render(requests, 'opt/seller.html', context=context)



def my_orders(request):
    if request.method == 'POST':
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            order_id = request.POST.get('order_id')
            try:
                order = Order.objects.get(id=order_id)
                order.status = form.cleaned_data['status']
                order.save()
                messages.success(request, '')
            except Order.DoesNotExist:
                messages.error(request, 'Order does not exist.')
            return redirect('my_orders')
    else:
        form = OrderStatusForm()

    if request.method == 'POST' and 'delete_order' in request.POST:
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, '')
        return redirect('my_orders')

    orders = Order.objects.all()
    for order in orders:
        if order.status.id == 1:
            order.default_status = order.status
        else:
            order.default_status = Status.objects.get(id=1)

        order.total_amount = calculate_order_total(order)  # Calculate total amount for each order
        order.total_quantity = calculate_order_quantity(order)  # Calculate total quantity for each order
    paginator = Paginator(orders, 5)  # Розділення списку замовлень на сторінки, по 5 замовлень на сторінці
    page_number = request.GET.get('page')  # Отримання номера поточної сторінки
    page_obj = paginator.get_page(page_number)  # Отримання об'єкту поточної сторінки
    context = {
        'title': 'Мої замовлення',
        'menu': menu_seller,
        'navi_seller': navi_seller,
        'form': form,
        'orders': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'opt/my_orders.html', context=context)



def print_order(request, order_id):
    order = Order.objects.get(id=order_id)
    items = []
    total = 0
    for item in order.items.all():
        item_total = item.quantity * item.price
        items.append({
            'item': item.good,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item_total,
        })
        total += item_total
    total_quantity = order.get_total_quantity()

    context = {
        'order': order,
        'items': items,
        'total': total,
        'shipping_address': order.address,
        'payment_method': order.payment_method,
        'total_quantity': total_quantity,
    }
    return render(request, 'opt/order_print.html', context=context)


def my_buyers(requests):
    context = {
        'title': 'Сторінка ОПТ',
        'menu': menu_seller,
        'navi_seller': navi_seller
    }
    return render(requests, 'opt/my_buyers.html', context=context)

def index(requests):
    context = {
        'title': 'Сторінка ОПТ',
        'menu': menu_seller,
        'navi_seller': navi_seller
    }
    return render(requests, 'opt/index.html', context=context)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Вернуть товары в базу данных
    for item in order.items.all():
        item.good.opt_stock += item.quantity  # Увеличить количество товара на количество в заказе
        item.good.save()

    order.delete()
    messages.success(request, '')
    return redirect('my_orders')