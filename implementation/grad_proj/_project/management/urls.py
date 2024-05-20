from django.urls import path
from . import views


urlpatterns = [
    path('manager',views.management, name='management' ),
    path('purchases',views.purchases, name='purchases' ),
    path('incomes',views.incomes, name='incomes' ),
    path('employees',views.employees, name='employees' ),
    path('expenses',views.expenses, name='expenses' ),

    path('update_employee/<int:id>',views.update_employee, name='update_employee' ),

    path('delete_income/<int:id>',views.delete_income, name='delete_income' ),
    path('delete_expense/<int:id>',views.delete_expense, name='delete_expense' ),
    path('delete_purchase/<int:id>',views.delete_purchase, name='delete_purchase' ),
    path('delete_employee/<int:id>',views.delete_employee, name='delete_employee' ),
]
