from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_image_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except:
        raise ValidationError("Invalid URL for this field")


class Course_Create(models.Model):
    author = models.ForeignKey('auth.User', blank=True, null=True)
    title = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=10, null=True)
    image_of_course = models.CharField(max_length=100, validators=[validate_image_url], null=True)
    description = models.TextField()

    def __str__(self):
        return self.title


def validate_youtube_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except:
        raise ValidationError("Invalid URL for this field")
    if "https://www.youtube.com/embed/" not in value:
        raise ValidationError("Invalid URL: That doesn't contain \"https://www.youtube.com/embed/\"")
    return value


class Videocreate(models.Model):
    course = models.ForeignKey(Course_Create)
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(max_length=200, validators=[validate_youtube_url])
    description = models.TextField()
    pub_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title