# Generated by Django 2.2.28 on 2024-01-31 11:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('account_number', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)], verbose_name='Kontonummer')),
                ('status', models.SmallIntegerField(choices=[(1, 'Avslått'), (2, 'Under behandling'), (3, 'Tilbakebetalt')], default=2, verbose_name='Tilbakebetalt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Utleggsdato')),
                ('store', models.CharField(max_length=50, verbose_name='Kjøpssted')),
                ('item', models.CharField(max_length=500, verbose_name='Varer')),
                ('event', models.CharField(max_length=50, verbose_name='Hensikt/Arragement')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Pris')),
                ('image', models.ImageField(upload_to='receipts', verbose_name='Kvittering')),
                ('refundrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='refund.RefundRequest')),
            ],
        ),
    ]
