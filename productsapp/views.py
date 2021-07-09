from django.shortcuts import render
from productsapp.models import Product, ProductCategory
import json
import os


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop',
        'site_name': 'GeekShop Store',
        'description': """Новые образы и лучшие бренды на GeekShop Store.
                        Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям."""
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'menu_items': ProductCategory.objects.values(),
        'productList': Product.objects.all()
    }
    return render(request, 'products/products.html', context)
