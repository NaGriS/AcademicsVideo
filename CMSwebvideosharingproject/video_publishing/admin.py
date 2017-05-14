from django.contrib import admin
from video_publishing.models import Course_Create
from video_publishing.models import Video_Create
from .models import  Comment

admin.site.register(Course_Create)
admin.site.register(Video_Create)

admin.site.register(Comment)