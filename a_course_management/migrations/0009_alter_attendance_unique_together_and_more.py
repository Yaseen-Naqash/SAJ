# Generated by Django 5.1.1 on 2024-10-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0008_attendance_session_section_session_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='session',
            field=models.CharField(blank=True, default='جلسه 1', max_length=31, null=True, verbose_name='جلسه'),
        ),
    ]
