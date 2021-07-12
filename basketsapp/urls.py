from django.urls import path
from basketsapp.views import basket_add

app_name = 'basketsapp'

urlpatterns = [
    path('add/<int:product_id>/', basket_add, name='basket_add'),
]
