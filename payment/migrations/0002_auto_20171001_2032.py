# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecustomer',
            name='stripe_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
