# Generated by Django 2.2.28 on 2023-10-13 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electofood', '0002_electionquestionform_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electionquestion',
            name='question',
            field=models.TextField(max_length=300, verbose_name='Påstand'),
        ),
    ]
