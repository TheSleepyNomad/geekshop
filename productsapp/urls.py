from django.urls import path
from .views import startPageView, productsPageView

app_name = 'productsapp'

urlpatterns = [
    path('', productsPageView.as_view(), name='index'),
    path('<int:category_id>/', productsPageView.as_view(), name='product'),
    path('page/<int:page>/', productsPageView.as_view(), name='page'),
]
