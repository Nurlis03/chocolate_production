from django.urls import path
from .views import *

urlpatterns = [
    path('employee/', employee_view, name='employee_list'),
    path('employee/update/<int:employee_id>/', employee_update, name='update_employee'),
    path('employee/delete/', delete_employee, name='delete_employee'),
    path('employee/add_employee/', add_employee, name='add_employee'),
]
