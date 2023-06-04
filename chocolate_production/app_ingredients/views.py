from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.urls import reverse


def ingredients(request):
    # Получаем список ингредиентов для отображения в шаблоне
    product_id = request.GET.get('product_id')
    error = request.GET.get('error')
    with connection.cursor() as cursor:
        cursor.execute(f'SP_GET_PRODUCT_INGREDIENTS @ProductID = {product_id}')
        result = cursor.fetchall()
        cursor.execute(f'GET_Name_Finished_products @id = {product_id}')
        product_name = cursor.fetchall()
        cursor.execute(f'GET_ID_Name_Raw_material')
        raw_materials = cursor.fetchall()
        cursor.execute('GET_ID_Name_Finished_products')
        products = cursor.fetchall()
        context = {
            'ingredients': result, 
            'product_id': product_id, 
            'product_name': product_name[0][0], 
            'raw_materials': raw_materials, 
            'products': products,
            'error': error
        }
        
    # Отображаем шаблон для отображения ингредиентов
    return render(request, 'ingredients.html', context)


def get_product_ingredients(request):
    # Получаем список всех продуктов для отображения в комбобоксе
    with connection.cursor() as cursor:
        cursor.execute('GET_ID_Name_Finished_products')
        products = cursor.fetchall()

    # Отображаем страницу с комбобоксом для выбора продукта
    return render(request, 'get_product_ingredients.html', {'products': products})  

def update_ingredient(request):
    if request.method == 'POST':
        # Получаем значения из POST-запроса
        ingredient_id = request.POST.get('ingredient_id')
        new_amount = request.POST.get('ingredient_amount')
        product_id = request.POST.get('product_id')
        # Выполняем хранимую процедуру для обновления ингредиента
        with connection.cursor() as cursor:
            cursor.execute(f'SP_UPDATE_Ingredient @IngredientID = {ingredient_id}, @Amount = {new_amount}')

        # После обновления ингредиента перенаправляем пользователя на страницу с ингредиентами продукта
        url = reverse('ingredients') + f'?product_id={product_id}'
        return redirect(url)


def delete_ingredient(request):
    ingredient_id = request.POST.get('ingredient_id_delete')
    product_id = request.POST.get('product_id_delete')

    cursor = connection.cursor()
    cursor.execute(f'SP_DELETE_Ingredient @id = {ingredient_id}')
    url = reverse('ingredients') + f'?product_id={product_id}'
    return redirect(url)


def add_ingredient(request):
    if request.method == 'POST':
        raw_material_id = request.POST['raw_material']
        amount = request.POST['amount']
        product_id = request.POST['product_id']
        cursor = connection.cursor()
        url = reverse('ingredients') + f'?product_id={product_id}'
        try:
            cursor.execute(f'SP_INSERT_Ingredient @ProductID = {product_id}, @Raw_materialID = {raw_material_id}, @Amount = {amount}')
        except IntegrityError:
            # Handling an exception that occurs when trying to insert a record that violates uniqueness into a unique index.
            # error_message = 'It is not possible to add an ingredient because such an ingredient already exists.'
            # messages.error(request, error_message)
            url += '&error=True'
            return redirect(url)
        return redirect(url)