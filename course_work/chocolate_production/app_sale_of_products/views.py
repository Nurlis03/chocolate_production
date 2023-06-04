from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

def sale_of_products_view(request):
    cursor = connection.cursor()
    cursor.execute('SP_READ_Sale_of_products')
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
        employee_id = request.POST['employee']
        cursor = connection.cursor()
        cursor.execute(f'SP_CheckToEnoughProducts @SellOfIDProduct = {product_id}, @NumberOfProductsSold = {amount}')
        result = cursor.fetchone()[0]
        if result == 1:
            cursor.execute(f'SP_SellProduct @SellOfIDProduct = {product_id}, @NumberOfProductsSold = {amount}, @EmployeeID = {employee_id}')

            # обновляем данные в объекте paginator
            data = cursor.execute('SP_READ_Sale_of_products').fetchall()
            paginator = Paginator(data, 10)
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj


            context['enough_products_modal'] = True
            return render(request, 'sale_of_products.html', context)
        else:
            context['not_enough_products_modal'] = True
            return render(request, 'sale_of_products.html', context)
    else:
        return render(request, 'sale_of_products.html', context)
        

