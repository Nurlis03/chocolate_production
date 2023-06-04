from django.urls import path
from .views import *

urlpatterns = [
    path('production_table/', production_view, name='url_production'),
]
