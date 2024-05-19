from django.shortcuts import render, redirect, get_object_or_404
from user.views import management_send_data
from .models import Income , Expense, Purchase
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
        "total_incomes" : total_incomes,
        "total_expenses" : total_expenses,
        "total_profit" : total_profit,
        "month_incomes" : month_incomes,
        "month_expenses" : month_expenses,
        "month_profit" : month_profit,
        "year_incomes" : year_incomes,
        "year_expenses" : year_expenses,
        "year_profit" : year_profit,
    }

    return render(request, "management/management.html", context)

def incomes(request):
    incomes = Income.objects.all()
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
    expenses = Expense.objects.all()
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
    purchases = Purchase.objects.all()
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
    
