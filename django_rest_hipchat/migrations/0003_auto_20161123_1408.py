# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_hipchat', '0002_auto_20161123_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('target', models.CharField(blank=True, max_length=255, null=True)),
                ('icon_url', models.URLField(blank=True, null=True)),
                ('icon_url_2x', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('key', models.CharField(blank=True, max_length=50, null=True)),
                ('homepage_url', models.URLField()),
                ('url', models.URLField()),
                ('scopes', models.CharField(choices=[('send_notification', 'send_notification')], max_length=50)),
                ('room_installable', models.BooleanField(default=True)),
                ('globally_installable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WebPanel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('panel_type', models.CharField(choices=[('sidebar', 'sidebar')], max_length=50)),
                ('key', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('location', models.CharField(default='hipchat.sidebar.right', max_length=255)),
                ('icon_url', models.URLField(blank=True, null=True)),
                ('icon_url_2x', models.URLField(blank=True, null=True)),
                ('integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='django_rest_hipchat.Integration')),
            ],
        ),
        migrations.AddField(
            model_name='glance',
            name='integration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glances', to='django_rest_hipchat.Integration'),
        ),
    ]
