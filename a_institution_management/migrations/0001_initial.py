# Generated by Django 5.1.1 on 2024-09-26 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('abbreviation_name', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=511, null=True)),
                ('latitude', models.CharField(max_length=63, null=True)),
                ('longitude', models.CharField(max_length=63, null=True)),
                ('Institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='a_institution_management.institution')),
            ],
        ),
    ]
