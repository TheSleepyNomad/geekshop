from basketsapp.models import Basket
from django.db.models import fields
from django.db import transaction
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ordersapp.forms import OrderItemsForm

from .models import Order, OrderItem

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
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity

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
    pass


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


class OrderDetail(DetailView):
    pass


def order_forming_complete(request, pk):
    pass
