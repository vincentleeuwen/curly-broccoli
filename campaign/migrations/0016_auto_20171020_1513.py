# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-20 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0015_referral_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='company',
            field=models.CharField(max_length=140),
        ),
    ]