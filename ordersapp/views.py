from django.http.response import HttpResponseRedirect
from basketsapp.models import Basket
from django.db.models import fields
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ordersapp.forms import OrderItemsForm
from productsapp.models import Product
from .models import Order, OrderItem
from django.http import JsonResponse

# Create your views here.


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop : Создание заказа'
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm,
                                                     extra=basket_items.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['products'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()

            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop : Создание заказа'
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.products.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


class OrderDetail(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))


def payment_result(request):
    status = request.GET.get('ik_inv_st')
    order_pk = request.GET.get('ik_pm_no')
    order_item = Order.objects.get(pk=order_pk)
    if status == 'success':
        order_item.status = Order.PAID
        order_item.save()
    if status == 'waitAccept':
        order_item.status = Order.PROCEED
        order_item.save()
    if status == 'canceled':
        order_item.status = Order.CANCEL
        order_item.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk)
        if product:
            return JsonResponse({'price'})
