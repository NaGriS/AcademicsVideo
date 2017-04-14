from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^courses/(?P<pk>[0-9]+)/$', views.video_list, name='video_list'),
    url(r'^courses/$', views.course_list, name='course_list'),
    url(r'^courses/new/$', views.course_new, name='course_new'),
    url(r'^courses/(?P<pk>[0-9]+)/edit/$', views.course_edit, name='course_edit'),
]