from django.urls import path
from .views import *

urlpatterns = [
    path('positions/', positions_view, name='positions_list'),
    path('positions/update/<int:position_id>/', position_update, name='position_update'),
    path('positions/delete/', position_delete, name='position_delete'),
    path('positions/add_position/', position_add, name='position_add'),
]
