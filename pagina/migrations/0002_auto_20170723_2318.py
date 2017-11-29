# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AddField(
            model_name='vote',
            name='choide_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.Choice'),
        ),
    ]
