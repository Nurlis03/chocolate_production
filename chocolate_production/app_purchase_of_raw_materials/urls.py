from django.urls import path
from .views import purchase_of_raw_materials_view

urlpatterns = [
    path('purchase_of_raw_materials/', purchase_of_raw_materials_view, name='purchase_of_raw_materials'),
]