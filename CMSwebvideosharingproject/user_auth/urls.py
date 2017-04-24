from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^$', views.redirect_to_login, name='redirect_to_login'),
    url(r'^register/$',views.UserFormView.as_view(),name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_view, name='logout_user'),

]