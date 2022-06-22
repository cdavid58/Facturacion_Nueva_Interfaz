# Generated by Django 3.2.8 on 2022-06-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentIdentification', models.TextField()),
                ('firstname', models.TextField()),
                ('surname', models.TextField()),
                ('address', models.TextField()),
                ('type_contract', models.TextField()),
                ('payroll_type_document_identification', models.TextField()),
                ('type_worker', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
                ('company', models.TextField()),
                ('salary', models.TextField()),
                ('user', models.TextField()),
                ('post', models.TextField()),
                ('hiring_date', models.TextField()),
                ('type', models.TextField()),
            ],
        ),
    ]