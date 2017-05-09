from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^courses/(?P<pk>[0-9]+)/$', views.video_list, name='video_list'),
    url(r'^courses/$', views.course_list, name='course_list'),
    url(r'^courses/new/$', views.course_new, name='course_new'),
    url(r'^courses/(?P<pk>[0-9]+)/edit/$', views.course_edit, name='course_edit'),
    url(r'^courses/(?P<course_pk>[0-9]+)/delete/$', views.course_delete, name='course_delete'),
    url(r'^courses/(?P<pk>[0-9]+)/new/$', views.video_new, name='video_new'),
    url(r'^courses/(?P<course_pk>[0-9]+)/(?P<video_pk>[0-9]+)/$', views.video, name='video'),
    url(r'^courses/(?P<course_pk>[0-9]+)/(?P<video_pk>[0-9]+)/edit/$', views.video_edit, name='video_edit'),
    url(r'^courses/(?P<course_pk>[0-9]+)/(?P<video_pk>[0-9]+)/delete/$', views.video_delete, name='video_delete'),
    #url(r'^search/',include('heystack.urls')),
]