from django.urls import path, include
from . import views

urlpatterns = [
    path('budget/', views.read_budget, name='budget'),
    path('budget/update/', views.update_budget, name='update_budget'),
]
