# Generated by Django 3.2.23 on 2024-05-17 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_income_purchase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='paid_money',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='money',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='money',
            new_name='amount',
        ),
    ]
