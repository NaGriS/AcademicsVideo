# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import videopublishing.models


class Migration(migrations.Migration):

    dependencies = [
        ('videopublishing', '0011_auto_20170424_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videocreate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('youtube_link', models.CharField(validators=[videopublishing.models.validate_youtube_url], max_length=200)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(to='videopublishing.Course_Create')),
            ],
        ),
        migrations.RemoveField(
            model_name='video_create',
            name='course',
        ),
        migrations.DeleteModel(
            name='Video_Create',
        ),
    ]
