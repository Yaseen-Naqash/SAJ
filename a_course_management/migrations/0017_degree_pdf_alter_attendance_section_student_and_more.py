# Generated by Django 5.1.1 on 2024-10-23 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0016_alter_sectionstudent_options'),
        ('a_user_management', '0007_alter_student_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='degree',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='Degrees/', verbose_name='فایل پیوست مدرک'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='section_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='a_course_management.sectionstudent', verbose_name='دانشجو'),
        ),
        migrations.AlterField(
            model_name='section',
            name='session_number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' تعداد جلسات برگزار شده '),
        ),
        migrations.AlterField(
            model_name='sectionstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_student', to='a_user_management.student', verbose_name='دانشجو'),
        ),
    ]
