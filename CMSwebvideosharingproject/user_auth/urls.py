from django.conf.urls import url

from . import views

urlpatterns=[
    #url(r'^register/$',views.UserFormView.as_view(),name='register'),
    #url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^index/$',views.UserFormView.as_view(),name='register'),
    url(r'^index/$', views.login_user, name='login_user'),
]