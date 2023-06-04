from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

# def purchase_of_raw_materials_view(request):
#     with connection.cursor() as cursor:
#         cursor.execute('SP_READ_Purchase_of_raw_materials')
#         data = cursor.fetchall()
#     context = {'data': data}
#     print(context)
#     return render(request, 'purchase_of_raw_materials.html', context)

def purchase_of_raw_materials_view(request):
    cursor = connection.cursor()
    cursor.execute('SP_READ_Purchase_of_raw_materials')
    data = cursor.fetchall()
    cursor.execute('GET_ID_Name_Raw_material')
    materials = cursor.fetchall()
    cursor.execute('GET_ID_Full_name_Employee')
    employees = cursor.fetchall()

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'materials': materials, 'employees': employees}

    if request.method == 'POST':
        raw_material_id = request.POST['raw_material']
        amount = request.POST['amount']
        cost_amount = request.POST['cost_amount']
        employee_id = request.POST['employee']

        cursor.execute(f'SP_Purchase @sum = {cost_amount}')
        result = cursor.fetchone()[0]

        if result == 0:
            cursor.execute(f'SP_INSERT_Purchase_of_raw_materials @raw_material = {raw_material_id}, @amount = {amount}, @cost_amount = {cost_amount}, @employee = {employee_id}')
            
            # обновляем данные в объекте paginator
            data = cursor.execute('SP_READ_Purchase_of_raw_materials').fetchall()
            paginator = Paginator(data, 10)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            
            context['show_modal'] = True
            return render(request, 'purchase_of_raw_materials.html', context)
        else:
            context['budget_modal'] = True
            return render(request, 'purchase_of_raw_materials.html', context)
    else:
        return render(request, 'purchase_of_raw_materials.html', context)

        

