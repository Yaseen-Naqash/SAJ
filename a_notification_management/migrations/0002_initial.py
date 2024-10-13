# Generated by Django 5.1.1 on 2024-10-12 00:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('a_course_management', '0002_initial'),
        ('a_notification_management', '0001_initial'),
        ('a_user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='a_user_management.employee'),
        ),
        migrations.AddField(
            model_name='notification',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='a_user_management.teacher'),
        ),
        migrations.AddField(
            model_name='notification',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='a_course_management.section'),
        ),
    ]
