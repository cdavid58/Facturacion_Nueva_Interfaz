# Generated by Django 3.2.8 on 2022-06-15 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_employee_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='company',
        ),
    ]
