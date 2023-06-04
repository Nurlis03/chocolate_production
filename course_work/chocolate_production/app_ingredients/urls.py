from django.urls import path
from .views import *

urlpatterns = [
    path('get_product_ingredients/', get_product_ingredients, name='get_product_ingredients'),
    path('update_ingredient/', update_ingredient, name='update_ingredient'),
    path('get_product_ingredients/ingredients/', ingredients, name='ingredients'),
    path('delete_ingredient/', delete_ingredient, name='delete_ingredient'),
    path('add_ingredient/', add_ingredient, name="add_ingredient"),
]
