# Generated by Django 5.1.1 on 2024-10-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_user_management', '0006_student_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='balance',
            field=models.IntegerField(default=0, null=True, verbose_name='(تومان) مبلغ'),
        ),
    ]
