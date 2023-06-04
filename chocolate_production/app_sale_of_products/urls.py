from django.urls import path
from .views import sale_of_products_view

urlpatterns = [
    path('sale_of_products/', sale_of_products_view, name='sale_of_products'),
]