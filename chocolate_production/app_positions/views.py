from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse


def get_positions(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute('SP_READ_Positions')
        results = cursor.fetchall()

    # Пагинация результатов
    paginator = Paginator(results, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'positions': page_obj}


def positions_view(request):
    return render(request, 'positions.html', get_positions(request))

# def raw_material_update(request, raw_material_id):
#     # Получаем данные о сырьи
#     cursor = connection.cursor()
#     cursor.execute("EXEC SP_FIND_Raw_material @raw_material_id=%s", [raw_material_id])
#     raw_material = cursor.fetchone()
#     context = {'raw_material': raw_material, **get_positions(request)}

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
#         return redirect('positions_list')
#     # Устанавливаем значение переменной show_modal в зависимости от значения параметра page
#     if 'page' in context:
#         context['show_modal'] = False
#     else:
#         context['show_modal'] = True

#     return render(request, 'positions.html', context)


def position_update(request, position_id):
    cursor = connection.cursor()
    cursor.execute("SP_FIND_Position @position_id=%s", [position_id])
    position = cursor.fetchone()
    context = {'position': position, **get_positions(request)}

    if request.method == 'POST':
        # Получаем новые данные сырья из формы
        position_id = request.POST['position_id']
        name_position = request.POST['name_position']

        cursor.execute(
            f"SP_UPDATE_Position @position_id = {position_id}, @name_position = '{name_position}'")
        connection.commit()

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('positions_list') + f'?page={page}'
            return HttpResponseRedirect(url)

        # Если параметр page не передан, перенаправляем пользователя на страницу списка сырья
        return redirect('positions_list')

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

    return render(request, 'positions.html', context)


def position_delete(request):
    if request.method == "POST":
        position_id_delete = request.POST['position_id_delete']
        cursor = connection.cursor()
        cursor.execute(f'SP_DELETE_Position @id = {position_id_delete}')

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('positions_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('positions_list')


def position_add(request):
    if request.method == 'POST':
        name_position = request.POST['name_position']

        cursor = connection.cursor()
        cursor.execute(f"SP_INSERT_Position @name_position = '{name_position}'")


        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('positions_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('positions_list')
