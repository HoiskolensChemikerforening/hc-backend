# Generated by Django 2.2.28 on 2023-09-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate', '0003_auto_20210428_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveSmallIntegerField(choices=[(1, 'Graduatestilling'), (2, 'Sommerjobb'), (3, 'Deltidsjobb')], unique=True)),
            ],
        ),
    ]
