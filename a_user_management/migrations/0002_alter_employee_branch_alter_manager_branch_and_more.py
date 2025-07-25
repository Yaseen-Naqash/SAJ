# Generated by Django 5.1.1 on 2025-07-12 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_institution_management', '0001_initial'),
        ('a_user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='a_institution_management.branch'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager', to='a_institution_management.branch'),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='a_institution_management.branch', verbose_name='شعبه'),
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='a_user_management.grade', verbose_name='سطح'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teachers', to='a_institution_management.branch'),
        ),
    ]
