# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-22 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomi', '0002_auto_20170522_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='results_declared',
            field=models.BooleanField(default=False),
        ),
    ]
