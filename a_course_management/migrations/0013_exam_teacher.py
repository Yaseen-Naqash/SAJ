# Generated by Django 5.1.1 on 2024-10-15 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0012_homework_description_homework_pdf_and_more'),
        ('a_user_management', '0005_person_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='a_user_management.teacher', verbose_name='استاد'),
        ),
    ]
