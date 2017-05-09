# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import videopublishing.models


class Migration(migrations.Migration):

    dependencies = [
        ('videopublishing', '0008_auto_20170414_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_create',
            name='youtube_link',
            field=models.CharField(max_length=200, validators=[videopublishing.models.validate_youtube_url]),
        ),
    ]
