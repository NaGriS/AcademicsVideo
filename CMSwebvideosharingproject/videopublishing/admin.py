from django.contrib import admin
from videopublishing.models import Course_Create
from videopublishing.models import Videocreate
from .models import  Comment

admin.site.register(Course_Create)
admin.site.register(Videocreate)

admin.site.register(Comment)