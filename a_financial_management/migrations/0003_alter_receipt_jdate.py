# Generated by Django 5.1.1 on 2024-10-19 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_financial_management', '0002_alter_receipt_options_receipt_jdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='jdate',
            field=models.CharField(default='1403/07/29', max_length=15, verbose_name='تاریخ'),
        ),
    ]
