# Generated by Django 2.2.24 on 2022-04-02 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('rentalservice', '0003_auto_20220402_1248'), ('rentalservice', '0004_auto_20220402_1319')]

    dependencies = [
        ('rentalservice', '0002_auto_20220304_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='client_nr',
            new_name='client_phone_nr',
        ),
        migrations.AlterField(
            model_name='rentalobject',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Utleieobjekt'),
        ),
        migrations.AlterField(
            model_name='rentalobject',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentalservice.Landlord', verbose_name='Komite'),
        ),
        migrations.AlterField(
            model_name='rentalobject',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rentalservice.RentalObjectType', verbose_name='Produkttype'),
        ),
        migrations.AlterField(
            model_name='rentalobjecttype',
            name='type',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]