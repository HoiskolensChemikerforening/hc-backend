# Generated by Django 2.2.28 on 2024-03-17 13:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchangepage', '0002_auto_20240317_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelletter',
            name='semester',
            field=models.CharField(max_length=7, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(7)], verbose_name='Semester'),
        ),
    ]