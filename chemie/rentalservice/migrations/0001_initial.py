# Generated by Django 2.2.10 on 2020-09-06 15:55

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('committees', '0003_auto_20180127_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='committees.Committee')),
            ],
        ),
        migrations.CreateModel(
            name='RentalObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Beskrivelse')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='rentalservice', verbose_name='Bilde')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentalservice.Landlord')),
            ],
        ),
    ]
