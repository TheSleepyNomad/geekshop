from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

# Create your views here.


class OrderList(ListView):
    pass


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
