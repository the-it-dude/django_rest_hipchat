# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 12:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_hipchat', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Integration',
            new_name='Installation',
        ),
    ]
