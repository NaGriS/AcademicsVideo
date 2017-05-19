from django import forms
from .models import Course_Create
from .models import Videocreate,Comment
from haystack.forms import SearchForm


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course_Create
        fields = ('title', 'year_of_study', 'image_of_course', 'description')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'input-group mb-2 mr-sm-2 mb-sm-0'})


class VideoForm(forms.ModelForm):

    class Meta:
        model = Videocreate
        fields = ('title', 'youtube_link', 'description',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
        
class NotesSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()