# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0002_auto_20170723_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote_text',
            field=models.CharField(default='', max_length=200),
        ),
    ]