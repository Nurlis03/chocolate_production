from django.shortcuts import render, redirect
from django.db import connection


def read_budget(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_READ_Budget")
        row = cursor.fetchone()
        data = {
            'budget_amount': row[1],
            'percentage': row[2],
            'bonus': row[3],
        }
    return render(request, 'budget_templates/budget.html', {'data': data})


def update_budget(request):
    if request.method == 'POST':
        budget_amount = request.POST.get('budget_amount')
        percentage = request.POST.get('percentage')
        bonus = request.POST.get('bonus')
        with connection.cursor() as cursor:
            cursor.execute("SP_UPDATE_Budget @Budget_amount = %s, @Percentage = %s, @Bonus = %s", (budget_amount, percentage, bonus))
        return redirect('budget')

