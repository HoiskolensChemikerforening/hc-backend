# Generated by Django 2.2.28 on 2024-08-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customprofile', '0019_auto_20240223_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='relationship_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Singel'), (2, 'Opptatt'), (3, 'Hemmelig!'), (4, 'HC forhold')], default=1, verbose_name='Samlivsstatus'),
        ),
    ]