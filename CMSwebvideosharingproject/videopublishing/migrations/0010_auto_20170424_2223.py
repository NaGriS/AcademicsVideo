# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-24 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videopublishing', '0009_auto_20170420_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_create',
            name='image_of_course',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course_create',
            name='year_of_study',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
