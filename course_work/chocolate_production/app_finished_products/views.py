from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse


def get_products(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute('SP_READ_Finished_products')
        results = cursor.fetchall()
        cursor.execute("SP_READ_Units")
        units = cursor.fetchall()

    # Пагинация результатов
    paginator = Paginator(results, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'products': page_obj, 'units': units}


def products_view(request):
    return render(request, 'finished_products.html', get_products(request))


def product_update(request, product_id):
    cursor = connection.cursor()
    cursor.execute("SP_FIND_product @product_id=%s", [product_id])
    product = cursor.fetchone()
    context = {'product': product, **get_products(request)}

    if request.method == 'POST':
        # Получаем новые данные сырья из формы
        product_id = request.POST['product_id']
        name_product = request.POST['name_product']
        unit_id = request.POST['unit_id']
        amount = request.POST['amount']
        cost_amount = request.POST['cost_amount']

        cursor.execute(f"SP_UPDATE_product @product_id = {product_id}, @name_product = '{name_product}', @unit_id = {unit_id}, @amount = {amount}, @cost_amount = {cost_amount}")
        connection.commit()

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('products_list') + f'?page={page}'
            return HttpResponseRedirect(url)

        # Если параметр page не передан, перенаправляем пользователя на страницу списка сырья
        return redirect('products_list')

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

    return render(request, 'finished_products.html', context)


def delete_product(request):
    if request.method == "POST":
        product_id_delete = request.POST['product_id_delete']
        cursor = connection.cursor()
        cursor.execute(f'SP_DELETE_product @id = {product_id_delete}')

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('products_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('products_list')


def add_product(request):
    if request.method == 'POST':
        name_product = request.POST['name_product']
        unit_id = request.POST['unit_id']
        amount = request.POST['amount']
        cost_amount = request.POST['cost_amount']

        cursor = connection.cursor()
        cursor.execute(f"SP_INSERT_product @name_product = '{name_product}', @unit_id = {unit_id}, @amount = {amount}, @cost_amount = '{cost_amount}'")


        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('products_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('products_list')
