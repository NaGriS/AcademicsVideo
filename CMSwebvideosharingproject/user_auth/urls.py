from django.conf.urls import url,patterns


from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^$', views.redirect_to_login, name='redirect_to_login'),
    url(r'^register/$',views.UserFormView.as_view(),name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_view, name='logout_user'),
    url(r'^password/$', views.change_password, name='change_password'),

]

urlpatterns += patterns('',
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'},name='password_reset_confirm'),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
         # ...
)