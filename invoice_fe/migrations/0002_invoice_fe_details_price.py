# Generated by Django 3.2.8 on 2022-06-23 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_fe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice_fe_details',
            name='price',
            field=models.TextField(default=3800),
        ),
    ]