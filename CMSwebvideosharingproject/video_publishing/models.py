from django.db import models
from django.utils import timezone


class Course_Create(models.Model):
    author = models.ForeignKey('auth.User', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Video_Create(models.Model):
    course = models.ForeignKey(Course_Create)
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
