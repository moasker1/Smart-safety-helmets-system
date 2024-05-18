from django.urls import path
from . import views


urlpatterns = [
    path('manager',views.management, name='management' ),
    path('purchases',views.purchases, name='purchases' ),
    path('incomes',views.incomes, name='incomes' ),
    path('expenses',views.expenses, name='expenses' ),
]
