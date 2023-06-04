from django.urls import path
from .views import *

urlpatterns = [
    path('units/', units_view, name='units_list'),
    path('units/update/<int:unit_id>/', unit_update, name='unit_update'),
    path('units/delete/', unit_delete, name='unit_delete'),
    path('units/add_unit/', unit_add, name='unit_add'),
]
