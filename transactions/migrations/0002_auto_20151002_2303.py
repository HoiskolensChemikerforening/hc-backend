# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'verbose_name_plural': 'Varer', 'verbose_name': 'Vare', 'ordering': ('_order',)},
        ),
        migrations.RemoveField(
            model_name='items',
            name='cover',
        ),
        migrations.AlterField(
            model_name='items',
            name='status_condition',
            field=models.IntegerField(verbose_name='Status', choices=[(1, 'Aktiv'), (0, 'Ikke aktiv')], max_length=2, default=1),
        ),
    ]
