from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse


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

    def get_cname(self):
        class_name = "course"
        return class_name

def validate_youtube_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except:
        raise ValidationError("Invalid URL for this field")
    if ("https://www.youtube.com/" not in value) and ("https://youtu.be/" not in value):
        raise ValidationError("Invalid URL: That doesn't contain \"https://www.youtube.com/\" or \"https://youtu.be/\"")
    return value

def get_cname(self):
        class_name = "course"
        return class_name


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

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    
    def get_cname(self):
        class_name = "video"
        return class_name
    
#    def get_absolute_url(self):
#       return ( str(self.course), str(self.pk) )

    def get_cname(self):
        class_name = "video"
        return class_name
    #def get_absolute_url(self):
    #    return reverse('video',
    #                   kwargs={'video': self.course})
    
#    def get_absolute_url(self):
#       return ( str(self.course), str(self.pk) )

class Comment(models.Model):
    post = models.ForeignKey(Videocreate, related_name='comments')
    author = models.CharField(max_length=200)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text