# Generated by Django 5.1.1 on 2024-10-15 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0005_alter_attendance_options_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='تاریخ'),
        ),
    ]
