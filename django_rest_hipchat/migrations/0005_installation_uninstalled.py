# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_hipchat', '0004_webhook'),
    ]

    operations = [
        migrations.AddField(
            model_name='installation',
            name='uninstalled',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
