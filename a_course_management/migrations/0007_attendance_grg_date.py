# Generated by Django 5.1.1 on 2024-10-15 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0006_alter_attendance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='grg_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
