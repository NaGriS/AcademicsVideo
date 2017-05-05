from django import forms
from .models import Course_Create
from .models import Video_Create


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course_Create
        fields = ('title', 'description', 'year_of_study', 'image_of_course')


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video_Create
        fields = ('title', 'youtube_link', 'description',)