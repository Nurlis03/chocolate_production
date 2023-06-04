from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse


def get_employees(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute('SP_READ_Employee')
        results = cursor.fetchall()
        # Получаем список должностей для combobox
        cursor.execute("SP_READ_Positions")
        positions = cursor.fetchall()

    # Пагинация результатов
    paginator = Paginator(results, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'employees': page_obj, 'positions': positions}


def employee_view(request):
    return render(request, 'employee.html', get_employees(request))

def employee_update(request,  employee_id):
    cursor = connection.cursor()
    cursor.execute("SP_FIND_Employee @employee_id=%s", [employee_id])
    employee = cursor.fetchone()
    context = {'employee': employee, **get_employees(request)}

    if request.method == 'POST':
        # Получаем новые данные сырья из формы
        employee_id = request.POST['employee_id']
        full_name = request.POST['full_name']
        job_title_id = request.POST['job_title']
        salary = request.POST['salary']
        address = request.POST['address']
        telephone = request.POST['telephone']

        cursor.execute(f"SP_UPDATE_Employee @ID = {employee_id}, @Full_name = '{full_name}', @Job_title = {job_title_id}, @Salary = {salary}, @Address = '{address}', @Telephone = '{telephone}'")
        connection.commit()

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('employee_list') + f'?page={page}'
            return HttpResponseRedirect(url)

        # Если параметр page не передан, перенаправляем пользователя на страницу списка сырья
        return redirect('employee_list')

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

    return render(request, 'employee.html', context)



def delete_employee(request):
    if request.method == "POST":
        employee_delete_id = request.POST['employee_delete_id']
        cursor = connection.cursor()
        cursor.execute(f'SP_DELETE_Employee @id = {employee_delete_id}')

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('employee_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        return redirect('employee_list')


def add_employee(request):
    cursor = connection.cursor()
    # Получаем список должностей для combobox
    cursor.execute("SP_READ_Positions")
    positions = cursor.fetchall()
    page_obj = get_employees(request)

    if request.method == 'POST':
        full_name = request.POST['full_name']
        job_title = request.POST['job_title']
        salary = request.POST['salary']
        address = request.POST['address']
        telephone = request.POST['telephone']

        cursor = connection.cursor()
        cursor.execute(f"SP_INSERT_Employee @FullName = '{full_name}', @JobTitle = {job_title}, @Salary = {salary}, @Address = '{address}', @Telephone = '{telephone}'")

        # Получаем значение параметра page из POST запроса
        page = request.POST.get('page')
        # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
        if page is not None:
            # Если параметр page передан, перенаправляем пользователя на соответствующую страницу
            url = reverse('employee_list') + f'?page={page}'
            return HttpResponseRedirect(url)
        
        
        return redirect('employee_list')

    return render(request, 'employee.html', {'positions': positions, 'employees': page_obj, 'show_add_modal': True})
