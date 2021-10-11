from django.http import request
from django.shortcuts import render
from django.views.generic.detail import DetailView
from productsapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404


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
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = ProductCategory.objects.values()
        context['num_of_page'] = [x for x in range(1,
                                                   context['paginator'].num_pages+1)]
        return context

    def get_queryset(self, *args, **kwargs):
        if 'category_id' in self.kwargs:
            category_id = get_object_or_404(ProductCategory,
                                            pk=self.kwargs['category_id'])
            return Product.objects.filter(category=category_id.pk)
        else:
            return Product.objects.all()


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
