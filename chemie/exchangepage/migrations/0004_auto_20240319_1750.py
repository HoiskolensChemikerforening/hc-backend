# Generated by Django 2.2.28 on 2024-03-19 16:50

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchangepage', '0003_auto_20240317_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='answer',
            field=ckeditor.fields.RichTextField(verbose_name='Svar'),
        ),
    ]