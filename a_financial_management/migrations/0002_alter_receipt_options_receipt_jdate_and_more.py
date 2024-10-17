# Generated by Django 5.1.1 on 2024-10-17 00:34

import jdatetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_financial_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receipt',
            options={'verbose_name': 'رسید مالی', 'verbose_name_plural': 'رسید های مالی'},
        ),
        migrations.AddField(
            model_name='receipt',
            name='jdate',
            field=models.CharField(default=jdatetime.datetime.now, max_length=15),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=11, null=True, verbose_name='(تومان) مبلغ'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='created_method',
            field=models.CharField(choices=[('0', 'اتوماتیک'), ('1', 'دستی')], default='1', max_length=1, verbose_name='روش ثبت'),
        ),
    ]