# Generated by Django 2.2.28 on 2023-03-29 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cgp', '0009_auto_20230329_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extravote',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extravote_group', to='cgp.Group'),
        ),
        migrations.AlterField(
            model_name='extravote',
            name='vote',
            field=models.ManyToManyField(blank=True, related_name='extravote_vote', to='cgp.Group'),
        ),
    ]