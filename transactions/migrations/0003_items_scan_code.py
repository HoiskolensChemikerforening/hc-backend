# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20151002_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='scan_code',
            field=models.PositiveIntegerField(verbose_name='Barkode', unique=True, default=1334),
            preserve_default=False,
        ),
    ]
