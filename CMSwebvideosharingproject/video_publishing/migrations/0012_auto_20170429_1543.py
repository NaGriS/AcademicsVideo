# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_publishing', '0011_auto_20170424_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_create',
            name='image_of_course',
        ),
        migrations.RemoveField(
            model_name='course_create',
            name='year_of_study',
        ),
    ]
