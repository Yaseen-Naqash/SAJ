# Generated by Django 5.1.1 on 2024-10-06 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_user_management', '0005_alter_admin_branch_alter_admin_institution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone2',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='person',
            name='randomCode',
            field=models.CharField(blank=True, default='0000', max_length=4, null=True),
        ),
    ]
