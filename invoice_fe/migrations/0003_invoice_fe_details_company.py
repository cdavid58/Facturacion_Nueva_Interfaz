# Generated by Django 3.2.8 on 2022-06-23 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_remove_company_passwd'),
        ('invoice_fe', '0002_invoice_fe_details_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice_fe_details',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
