# Generated by Django 3.2.23 on 2024-05-17 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20240518_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='purchase_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
