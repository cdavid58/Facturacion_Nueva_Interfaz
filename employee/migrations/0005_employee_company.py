# Generated by Django 3.2.8 on 2022-06-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_remove_employee_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.TextField(default=''),
        ),
    ]
