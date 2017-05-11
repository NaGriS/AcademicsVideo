from django import forms
from .models import Course_Create
from .models import Video_Create,Comment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course_Create
        fields = ('title', 'year_of_study', 'image_of_course', 'description')


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video_Create
        fields = ('title', 'youtube_link', 'description',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
