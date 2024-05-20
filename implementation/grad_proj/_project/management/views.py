from django.shortcuts import render, redirect, get_object_or_404
from user.views import management_send_data
from .models import *
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime,timedelta

def management(request):
    current_date = timezone.now()

    start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

    start_of_year = current_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = current_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    workers_num = Employee.objects.filter(job="worker").count()
    supervisors_num = Employee.objects.filter(job="supervisor").count()

    total_salaries = Employee.objects.all().aggregate(Sum('salary'))['salary__sum'] or 0
    total_incomes = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_profit = total_incomes - total_expenses

    month_incomes = Income.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_expenses = Expense.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    month_profit = month_incomes - month_expenses

    year_incomes = Income.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_expenses = Expense.objects.filter(date__gte=start_of_year, date__lte=end_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    year_profit = year_incomes - year_expenses

    context = {
        "total_salaries" : total_salaries,
        "total_incomes" : total_incomes,
        "total_expenses" : total_expenses,
        "total_profit" : total_profit,
        "month_incomes" : month_incomes,
        "month_expenses" : month_expenses,
        "month_profit" : month_profit,
        "year_incomes" : year_incomes,
        "year_expenses" : year_expenses,
        "year_profit" : year_profit,
        "workers_num" : workers_num,
        "supervisors_num" : supervisors_num,
    }

    return render(request, "management/management.html", context)

def incomes(request):
    incomes = Income.objects.all().order_by("-date")
    if "addIncome" in request.POST:
        site  = request.POST.get("site")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Income.objects.create(site = site, amount = amount, date = date)
        messages.success(request, "income added succesfully")
        return redirect("incomes")
    context = {"incomes" : incomes}
    return render(request, "management/incomes.html", context)

def expenses(request):
    expenses = Expense.objects.all().order_by("-date")
    if "addExpense" in request.POST:
        expense_type  = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Expense.objects.create(expense_type = expense_type, amount = amount, date = date)
        messages.success(request, "Expense added succesfully")
        return redirect("expenses")
    context = {"expenses" : expenses}
    return render(request, "management/expenses.html", context)

def purchases(request):
    purchases = Purchase.objects.all().order_by("-date")
    if "addPurchase" in request.POST:
        site  = request.POST.get("site")
        purchase_type  = request.POST.get("purchase_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        Purchase.objects.create(site=site , purchase_type = purchase_type, amount = amount, date = date)
        messages.success(request, "Purchase added succesfully")
        return redirect("purchases")
    context = {"purchases" : purchases}
    return render(request, "management/purchases.html", context)

def employees(request):
    employees = Employee.objects.all()
    if "addEmployee" in request.POST:
        name  = request.POST.get("name")
        salary  = request.POST.get("salary")
        job = request.POST.get("job")
        Employee.objects.create(name=name , salary = salary, job = job , remain_salary = salary)
        messages.success(request, "Employee added succesfully")
        return redirect("employees")
    context = {"employees" : employees}
    return render(request, "management/employees.html", context)
# ==============================================================================
def update_employee(request, id):
    if "updateEmployee" in request.POST:
        name = request.POST.get("name")
        salary = request.POST.get("salary")
        remain_salary = request.POST.get("remain_salary")
        job = request.POST.get("job")

        employee = Employee.objects.get(id=id)
        employee.name=name
        employee.salary=salary
        employee.remain_salary = remain_salary
        employee.job=job
        employee.save()

        messages.success(request, "Employee Updated successfully")
        return redirect("employees")
# ==============================================================================
def delete_income(request, id):
    income_to_delete = get_object_or_404(Income, id =id )
    income_to_delete.delete()
    messages.success(request, "Income deleted successfully")
    return redirect("incomes")

def delete_expense(request, id):
    expense_to_delete = get_object_or_404(Expense, id =id )
    expense_to_delete.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("expenses")

def delete_purchase(request, id):
    purchase_to_delete = get_object_or_404(Purchase, id =id )
    purchase_to_delete.delete()
    messages.success(request, "purchase deleted successfully")
    return redirect("purchases")

def delete_employee(request, id):
    employee_to_delete = get_object_or_404(Employee, id =id )
    employee_to_delete.delete()
    messages.success(request, "employee deleted successfully")
    return redirect("employees")
    
