# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0003_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('user', models.ForeignKey(verbose_name='Kontoinnehaver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='pages.Page')),
                ('status_condition', models.CharField(verbose_name='Status', choices=[(1, 'Aktiv'), (0, 'Ikke aktiv')], default=1, max_length=1)),
                ('published_date', models.DateTimeField(verbose_name='Publisert', auto_now_add=True)),
                ('picture', models.ImageField(upload_to='')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Pris')),
                ('cover', models.ImageField(upload_to='items')),
                ('author', models.ForeignKey(verbose_name='Opprettet av', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('account', models.ForeignKey(to='transactions.Accounts')),
                ('item_list', models.ManyToManyField(to='transactions.Items')),
            ],
        ),
    ]
