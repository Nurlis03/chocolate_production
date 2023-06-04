from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

def production_view(request):
    cursor = connection.cursor()
    cursor.execute('SP_READ_Production')
    data = cursor.fetchall()
    cursor.execute('GET_ID_Name_Finished_products')
    products = cursor.fetchall()
    cursor.execute('GET_ID_Full_name_Employee')
    employees = cursor.fetchall()
    
    paginator = Paginator(data, 10)  # разбиваем данные на страницы, по 10 элементов на страницу
    
    page_number = request.GET.get('page')  # получаем номер текущей страницы из параметра 'page' в URL
    
    page_obj = paginator.get_page(page_number)  # получаем объект страницы, соответствующей номеру

    context = {'page_obj': page_obj, 'products': products, 'employees': employees}  # передаем объект страницы в контекст шаблона
        
    if request.method == 'POST':
        product_id = request.POST['product_id']
        amount = request.POST['amount']
        employee_id = request.POST['employee_id']
        cursor = connection.cursor()
        cursor.execute(f"SP_check_raw_material_for_production @product_id = {product_id}, @product_amount = {amount}")
        result = cursor.fetchone()[0]
        if result == 1:
            cursor.execute(f'SP_INSERT_Production @product = {product_id}, @amount = {amount},  @employee = {employee_id}')

            # обновляем данные в объекте paginator
            data = cursor.execute('SP_READ_Production').fetchall()
            paginator = Paginator(data, 10)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj

            context['show_modal'] = True
            return render(request, 'production.html', context)
        elif result == -1:
            context['no_raw_materials_modal'] = True
            return render(request, 'production.html', context) 
        else:
            context['not_enough_raw_materials_modal'] = True
            return render(request, 'production.html', context)
    else:
        return render(request, 'production.html', context)
        

