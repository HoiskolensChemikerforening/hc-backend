# Generated by Django 2.2.24 on 2022-09-17 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customprofile', '0014_merge_20220907_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='specialization',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Ingen'), (2, 'Analytisk kjemi'), (3, 'Anvendt teoretisk kjemi'), (4, 'Bioteknologi'), (5, 'Materialkjemi og energiteknologi'), (6, 'Organisk kjemi'), (7, 'Kjemisk prosessteknologi')], default=1, verbose_name='Spesialisering'),
        ),
    ]