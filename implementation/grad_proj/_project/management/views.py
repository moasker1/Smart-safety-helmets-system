from django.shortcuts import render, redirect
from user.views import management_send_data
from .models import Income , Expense, Purchase
from django.contrib import messages

def management(request):
    return render(request, "management/management.html")

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
