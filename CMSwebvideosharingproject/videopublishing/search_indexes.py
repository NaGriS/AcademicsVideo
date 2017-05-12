import datetime
from haystack import indexes
from videopublishing.models import Videocreate

class VideocreateIndex(indexes.SearchIndex, indexes.Indexable):
     text = indexes.CharField(document=True, use_template=True)
     title = indexes.CharField(model_attr='title') 
     pub_date = indexes.DateTimeField(model_attr='pub_date')
     #description = indexes.TextField()
     #description = indexes.TextField(model_attr='description')
     
     content_auto = indexes.EdgeNgramField(model_attr='title')
     
     def get_model(self):
          return Videocreate
     
     def index_queryset(self, using=None):
          """Used when the entire index for model is updated."""
          return self.get_model().objects.all()
     