# Generated by Django 5.1.1 on 2024-12-03 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0003_remove_section_end_date_remove_section_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionstudent',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ پایان'),
        ),
        migrations.AlterField(
            model_name='sectionstudent',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ شروع'),
        ),
    ]
