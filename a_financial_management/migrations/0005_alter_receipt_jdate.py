# Generated by Django 5.1.1 on 2025-03-28 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_financial_management', '0004_alter_receipt_jdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='jdate',
            field=models.CharField(default='1404/01/08', max_length=15, verbose_name='تاریخ'),
        ),
    ]
