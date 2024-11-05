# Generated by Django 5.1.1 on 2024-11-04 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_course_management', '0018_alter_sectiontimeslot_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.CharField(max_length=127, null=True, verbose_name='قیمت ثبت نام به تومان'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='j_create_date',
            field=models.CharField(default='1403/08/15', max_length=15, verbose_name='تاریخ صدور'),
        ),
    ]
