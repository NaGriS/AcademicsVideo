import datetime
from django.utils import timezone
from haystack import indexes
from videopublishing.models import Videocreate

class VideocreateIndex(indexes.SearchIndex, indexes.Indexable):
     text = indexes.CharField(document=True, use_template=True)
     title = indexes.EdgeNgramField(model_attr='title')
     description = indexes.EdgeNgramField(model_attr='description')
     pub_date = indexes.DateTimeField(model_attr='pub_date',null=True)
     #course = indexes.CharField()
     #youtube_link = indexes.CharField(model_attr='youtube_link')
     #description = indexes.CharField(model_attr='description')
     #description = indexes.TextField()
     #content_auto = indexes.EdgeNgramField(model_attr='title')
     
     def get_model(self):
          return Videocreate
     
     #def prepare_course_title(self, obj):
     #     return [ course.title for a in obj.course.all()]
     #def prepare_course_title(self, obj):
     #     return obj.course.title
     
     
     def index_queryset(self, using=None):
          """Used when the entire index for model is updated."""
          #return self.get_model().objects.all()
          #"""Used when the entire index for model is updated."""
          return self.get_model().objects.filter(pub_date__lte=timezone.now())
          