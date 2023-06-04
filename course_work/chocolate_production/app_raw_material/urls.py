from django.urls import path
from .views import *

urlpatterns = [
    path('raw_materials/', raw_material_view, name='raw_materials_list'),
    path('raw_materials/update/<int:raw_material_id>/', raw_material_update, name='raw_material_update'),
    path('raw_materials/delete/', delete_raw_material, name='delete_raw_material'),
    path('raw_materials/add_raw_material/', add_raw_material, name='add_raw_material'),
]
