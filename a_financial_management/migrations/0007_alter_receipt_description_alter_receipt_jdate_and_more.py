# Generated by Django 5.1.1 on 2024-11-17 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_financial_management', '0006_receipt_formatted_amount_alter_receipt_confirmed_and_more'),
        ('a_user_management', '0009_alter_phoneverification_options_alter_grade_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='description',
            field=models.TextField(blank=True, default='', max_length=511, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='jdate',
            field=models.CharField(default='1403/08/28', max_length=15, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='payer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='a_user_management.student', verbose_name='پرداخت کننده'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='payment_method',
            field=models.CharField(choices=[('0', 'کارتخوان'), ('1', 'کارت به کارت'), ('2', 'نقدی'), ('3', 'درگاه پرداخت'), ('4', 'تخفیفی')], default='0', max_length=1, verbose_name='روش پرداخت'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='title',
            field=models.CharField(max_length=63, null=True, verbose_name='عنوان'),
        ),
    ]
