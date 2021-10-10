from django.http import request
from django.shortcuts import render
from productsapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView


# Create your views here.
class startPageView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {
        'title': 'GeekShop',
        'site_name': 'GeekShop Store',
        'description': """Новые образы и лучшие бренды на GeekShop Store.
                        Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям."""
    }


# def index(request):
#     context = {
#         'title': 'GeekShop',
#         'site_name': 'GeekShop Store',
#         'description': """Новые образы и лучшие бренды на GeekShop Store.
#                         Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям."""
#     }
#     return render(request, 'products/index.html', context)

class productsPageView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    extra_context = {'title': 'GeekShop - Каталог'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = ProductCategory.objects.values()
        return context


# def products(request, category_id=None, page=1):
#     context = {'title': 'GeekShop - Каталог',
#                'menu_items': ProductCategory.objects.values(), }
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()
#     paginator = Paginator(products, 3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context['products'] = products_paginator
#     return render(request, 'products/products.html', context)
