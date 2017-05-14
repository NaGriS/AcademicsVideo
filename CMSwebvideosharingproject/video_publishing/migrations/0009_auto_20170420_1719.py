# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import video_publishing.models


class Migration(migrations.Migration):

    dependencies = [
        ('video_publishing', '0008_auto_20170414_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_create',
            name='youtube_link',
            field=models.CharField(max_length=200, validators=[video_publishing.models.validate_youtube_url]),
        ),
    ]
