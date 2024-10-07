# Generated by Django 5.1.1 on 2024-10-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_user_management', '0006_person_phone2_person_randomcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('verification_code', models.CharField(blank=True, max_length=4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
