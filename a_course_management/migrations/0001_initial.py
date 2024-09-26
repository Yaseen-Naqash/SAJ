# Generated by Django 5.1.1 on 2024-09-26 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('a_user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(max_length=2047, null=True)),
                ('course_img', models.ImageField(blank=True, null=True, upload_to='Course_images/')),
                ('prerequisites', models.ManyToManyField(related_name='required_for', to='a_course_management.course')),
                ('teachers', models.ManyToManyField(related_name='courses', to='a_user_management.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ClassSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_sessions', to='a_course_management.course')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='a_course_management.course')),
            ],
        ),
    ]
