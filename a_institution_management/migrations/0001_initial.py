# Generated by Django 5.1.1 on 2025-07-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=511, null=True)),
                ('latitude', models.CharField(max_length=63, null=True)),
                ('longitude', models.CharField(max_length=63, null=True)),
            ],
            options={
                'verbose_name': 'شعبه',
                'verbose_name_plural': 'شعب',
            },
        ),
    ]
