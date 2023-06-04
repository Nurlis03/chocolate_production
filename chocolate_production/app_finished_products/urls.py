from django.urls import path
from .views import *

urlpatterns = [
    path('products/', products_view, name='products_list'),
    path('products/update/<int:product_id>/', product_update, name='product_update'),
    path('products/delete/', delete_product, name='delete_product'),
    path('products/add_product/', add_product, name='add_product'),
]
