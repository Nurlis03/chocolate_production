from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse


def get_raw_materials(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute('SP_READ_Raw_material')
        results = cursor.fetchall()
        cursor.execute("SP_READ_Units")
        units = cursor.fetchall()

    # Пагинация результатов
    paginator = Paginator(results, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'raw_materials': page_obj, 'units': units}


def raw_material_view(request):
    return render(request, 'raw_materials.html', get_raw_materials(request))

# def raw_material_update(request, raw_material_id):
#     # Получаем данные о сырьи
#     cursor = connection.cursor()
#     cursor.execute("EXEC SP_FIND_Raw_material @raw_material_id=%s", [raw_material_id])
#     raw_material = cursor.fetchone()
#     context = {'raw_material': raw_material, **get_raw_materials(request)}

#     if 'page' in request.GET:
#         context['page'] = request.GET['page']
#     if request.method == 'POST':
#         # Получаем новые данные сырьи из формы
#         raw_material_id = request.POST['raw_material_id']
#         name_raw_material = request.POST['name_raw_material']
#         unit_id = request.POST['unit_id']
#         amount = request.POST['amount']
#         cost_amount = request.POST['cost_amount']

#         cursor.execute(f"EXEC SP_UPDATE_Raw_material @raw_material_id = {raw_material_id}, @name_raw_material = '{name_raw_material}', @unit_id = {unit_id}, @amount = {amount}, @cost_amount = {cost_amount}")
#         connection.commit()

#         # Перенаправляем пользователя на страницу списка сырья
#         return redirect('raw_materials_list')
#     # Устанавливаем значение переменной show_modal в зависимости от значения параметра page
#     if 'page' in context:
#         context['show_modal'] = False
#     else:
#         context['show_modal'] = True

#     return render(request, 'raw_materials.html', context)


def raw_material_update(request, raw_material_id):
    cursor = connection.cursor()
    cursor.execute("SP_FIND_Raw_material @raw_material_id=%s", [raw_material_id])
    raw_material = cursor.fetchone()
    context = {'raw_material': raw_material, **get_raw_materials(request)}

    if request.method == 'POST':
        # Получаем новые данные сырья из формы
        raw_material_id = request.POST['raw_material_id']
        name_raw_material = request.POST['name_raw_material']
        unit_id = request.POST['unit_id']
        amount = request.POST['amount']
        cost_amount = request.POST['cost_amount']

        cursor.execute(
            f"SP_UPDATE_Raw_material @raw_material_id = {raw_material_id}, @name_raw_material = '{name_raw_material}', @unit_id = {unit_id}, @amount = {amount}, @cost_amount = {cost_amount}")
        connection.commit()

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('raw_materials_list') + f'?page={page}'
            return HttpResponseRedirect(url)

        # Если параметр page не передан, перенаправляем пользователя на страницу списка сырья
        return redirect('raw_materials_list')

    # Получаем значение параметра page из GET запроса
    page = request.GET.get('page')
    if page is None:
        # Если параметр page не передан, устанавливаем значение переменной show_modal в True
        context['show_modal'] = True
    else:
        # Если параметр page передан, устанавливаем значение переменной show_modal в False
        context['show_modal'] = False
    # Проверяем наличие параметра 'show_modal' в GET-запросе и устанавливаем соответствующее значение переменной
    if 'show_modal' in request.GET:
        context['show_modal'] = True

    return render(request, 'raw_materials.html', context)


def delete_raw_material(request):
    if request.method == "POST":
        raw_material_id_delete = request.POST['raw_material_id_delete']
        cursor = connection.cursor()
        cursor.execute(f'SP_DELETE_Raw_material @id = {raw_material_id_delete}')

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('raw_materials_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('raw_materials_list')


def add_raw_material(request):
    if request.method == 'POST':
        name_raw_material = request.POST['name_raw_material']
        unit_id = request.POST['unit_id']
        amount = request.POST['amount']
        cost_amount = request.POST['cost_amount']

        cursor = connection.cursor()
        cursor.execute(f"SP_INSERT_Raw_material @name_raw_material = '{name_raw_material}', @unit_id = {unit_id}, @amount = {amount}, @cost_amount = '{cost_amount}'")


        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('raw_materials_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('raw_materials_list')
