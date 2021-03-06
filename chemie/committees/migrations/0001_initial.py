# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 19:01
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='komiteer')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('one_liner', models.CharField(max_length=30, verbose_name='Lynbeskrivelse')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Beskrivelse')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='committees.Committee')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Stillingsnavn')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Epost')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='committees.Committee')),
                ('permission_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='position',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='committee', chained_model_field='committee', on_delete=django.db.models.deletion.CASCADE, to='committees.Position'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
