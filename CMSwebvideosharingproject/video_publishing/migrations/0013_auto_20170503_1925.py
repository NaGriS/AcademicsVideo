# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import video_publishing.models


class Migration(migrations.Migration):

    dependencies = [
        ('video_publishing', '0012_auto_20170429_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_create',
            name='image_of_course',
            field=models.CharField(max_length=100, validators=[video_publishing.models.validate_image_url], null=True),
        ),
        migrations.AddField(
            model_name='course_create',
            name='year_of_study',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
