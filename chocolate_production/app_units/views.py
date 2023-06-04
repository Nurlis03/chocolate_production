from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse


def get_units(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute('SP_READ_Units')
        results = cursor.fetchall()

    # Пагинация результатов
    paginator = Paginator(results, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'units': page_obj}


def units_view(request):
    return render(request, 'units.html', get_units(request))

def unit_update(request, unit_id):
    cursor = connection.cursor()
    cursor.execute("SP_FIND_Unit @unit_id=%s", [unit_id])
    unit = cursor.fetchone()
    context = {'unit': unit, **get_units(request)}

    if request.method == 'POST':
        # Получаем новые данные сырья из формы
        unit_id = request.POST['unit_id']
        name_unit = request.POST['name_unit']

        cursor.execute(f"SP_UPDATE_Unit @unit_id = {unit_id}, @name_unit = '{name_unit}'")
        connection.commit()

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('units_list') + f'?page={page}'
            return HttpResponseRedirect(url)

        # Если параметр page не передан, перенаправляем пользователя на страницу списка сырья
        return redirect('units_list')

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

    return render(request, 'units.html', context)


def unit_delete(request):
    if request.method == "POST":
        unit_id_delete = request.POST['unit_id_delete']
        cursor = connection.cursor()
        cursor.execute(f'SP_DELETE_Unit @id = {unit_id_delete}')

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('units_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('units_list')


def unit_add(request):
    if request.method == 'POST':
        name_unit = request.POST['name_unit']

        cursor = connection.cursor()
        cursor.execute(f"SP_INSERT_Unit @name_unit = '{name_unit}'")


        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('units_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('units_list')
