# Generated by Django 5.1.1 on 2024-10-06 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_user_management', '0007_phoneverification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='institution',
        ),
        migrations.AddField(
            model_name='student',
            name='education',
            field=models.CharField(blank=True, choices=[('0', 'ابتدایی'), ('1', 'متوسطه اول'), ('2', 'متوسطه دوم'), ('3', 'دیپلم'), ('4', 'کاردانی'), ('5', 'کارشناسی'), ('6', 'کارشناسی ارشد'), ('7', 'دکتری')], max_length=1, null=True),
        ),
    ]
