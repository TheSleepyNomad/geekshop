from django.db.models import fields
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Order

# Create your views here.


class OrderList(ListView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DeleteView):
    pass


class OrderDetail(DetailView):
    pass


def order_forming_complete(request, pk):
    pass
