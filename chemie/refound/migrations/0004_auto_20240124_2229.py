# Generated by Django 2.2.28 on 2024-01-24 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refound', '0003_auto_20240124_2228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refoundrequest',
            old_name='paystatus',
            new_name='status',
        ),
    ]