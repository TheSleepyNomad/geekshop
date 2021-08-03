from django.urls import path
from basketsapp.views import basket_add, basket_del, basket_edit

app_name = 'basketsapp'

urlpatterns = [
    path('add/<int:product_id>/', basket_add, name='basket_add'),
    path('remove/<int:id>/', basket_del, name='basket_del'),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
