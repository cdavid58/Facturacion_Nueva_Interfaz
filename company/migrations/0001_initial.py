# Generated by Django 3.2.8 on 2022-06-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_identification', models.TextField()),
                ('dv', models.TextField()),
                ('business_name', models.TextField()),
                ('merchant_registration', models.TextField()),
                ('address', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
                ('type_document_identification', models.TextField()),
                ('type_organization', models.TextField()),
                ('type_regime', models.TextField()),
                ('certificate_generation_date', models.TextField()),
                ('certificate_expiration_date', models.TextField()),
                ('resolution_generation_date', models.TextField()),
                ('resolution_expiration_date', models.TextField()),
                ('resolution_number', models.TextField()),
                ('prefix', models.TextField()),
            ],
        ),
    ]