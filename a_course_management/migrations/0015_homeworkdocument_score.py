# Generated by Django 5.1.1 on 2024-10-15 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0014_alter_sectionstudent_options_homeworkdocument_seen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworkdocument',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
