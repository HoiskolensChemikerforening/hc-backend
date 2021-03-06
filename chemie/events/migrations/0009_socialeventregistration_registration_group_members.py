# Generated by Django 2.2.13 on 2021-02-17 15:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_auto_20210217_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialeventregistration',
            name='registration_group_members',
            field=models.ManyToManyField(blank=True, related_name='registration_group_members', to=settings.AUTH_USER_MODEL, verbose_name='Møtende medlemmer på arrangement'),
        ),
    ]
