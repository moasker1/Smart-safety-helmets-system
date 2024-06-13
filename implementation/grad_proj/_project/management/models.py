from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    expense_type  = models.CharField(max_length=100, blank=True, null=True)

class Income(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
class Purchase(models.Model):
    site  = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    purchase_type  = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

class Employee(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    remain_salary = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)

class RecentAction(models.Model):
    user = models.CharField(max_length=100,blank=True, null=True)  
    action_type = models.CharField(max_length=100,blank=True, null=True)  
    action_sort = models.CharField(max_length=100,blank=True, null=True)  
    model_affected = models.CharField(max_length=100,blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)