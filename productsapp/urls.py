from django.urls import path
from productsapp.views import products

app_name = 'productsapp'

urlpatterns = [
    path('', products, name='index')
]
