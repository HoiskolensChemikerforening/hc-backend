# Generated by Django 2.2.13 on 2021-08-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merch', '0001_initial'),
    ]


    operations = [
        migrations.AlterField(
            model_name='merch',
            name='price',
            field=models.FloatField(),
        ),
    ]