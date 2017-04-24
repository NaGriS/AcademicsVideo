from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class Course_Create(models.Model):
    author = models.ForeignKey('auth.User', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


def validate_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except:
        raise ValidationError("Invalid URL for this field")
    if not "https://www.youtube.com/embed/" in value:
        raise ValidationError("Invalid URL: That doesn't contain \"https://www.youtube.com/embed/\"")
    return value

class Video_Create(models.Model):
    course = models.ForeignKey(Course_Create)
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(max_length=200, validators=[validate_url])
    description = models.TextField()
    pub_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title