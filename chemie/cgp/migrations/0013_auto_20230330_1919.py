# Generated by Django 2.2.28 on 2023-03-30 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cgp', '0012_auto_20230330_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='vote',
        ),
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.ManyToManyField(related_name='mainvote', to='cgp.Group'),
        ),
    ]