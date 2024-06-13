from django.urls import path
from . import views


urlpatterns = [
    path('manager',views.management, name='management' ),
    path('purchases',views.purchases, name='purchases' ),
    path('incomes',views.incomes, name='incomes' ),
    path('employees',views.employees, name='employees' ),
    path('expenses',views.expenses, name='expenses' ),
    path('analytics',views.analytics, name='analytics' ),

    path('update_employee/<int:id>',views.update_employee, name='update_employee' ),
    path('update_expense/<int:id>',views.update_expense, name='update_expense' ),
    path('update_income/<int:id>',views.update_income, name='update_income' ),
    path('update_purchase/<int:id>',views.update_purchase, name='update_purchase' ),

    path('delete_income/<int:id>',views.delete_income, name='delete_income' ),
    path('delete_expense/<int:id>',views.delete_expense, name='delete_expense' ),
    path('delete_purchase/<int:id>',views.delete_purchase, name='delete_purchase' ),
    path('delete_employee/<int:id>',views.delete_employee, name='delete_employee' ),
]
