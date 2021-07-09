from django.contrib import admin
from productsapp.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)