# Generated by Django 5.1.1 on 2024-12-24 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0005_alter_attendance_section_and_more'),
        ('a_financial_management', '0002_initial'),
        ('a_user_management', '0002_alter_teacher_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='reason',
            field=models.CharField(blank=True, choices=[('0', 'بابت قسط شهریه'), ('1', 'بابت شهریه'), ('2', 'بابت کلاس تقویتی'), ('3', 'بابت کمک به آموزشگاه'), ('4', 'بابت خسارت'), ('5', 'نامشخص')], default='5', max_length=1, null=True, verbose_name='بابت'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to='a_course_management.section', verbose_name='دوره'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='jdate',
            field=models.CharField(default='1403/10/04', max_length=15, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='payer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to='a_user_management.student', verbose_name='پرداخت کننده'),
        ),
    ]
