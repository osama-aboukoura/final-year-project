from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^activate/$', views.activate, name='activate'),
    url(r'^reset-password/$', views.reset_password, name='reset_password'),
    url(r'^reset-password-auth/$', views.reset_password_auth, name='reset_password_auth'),
    url(r'^reset-password-confirm/$', views.reset_password_confirm, name='reset_password_confirm'),
    url(r'^profile/(?P<user>[A-Za-z0-9]+)$', views.profileInfo, name='profile'),    
    url(r'^edit-profile/(?P<user>[A-Za-z0-9]+)$', views.editprofileInfo, name='edit-profile'),    
    url(r'^flagged-posts/$', views.flaggedPostsView, name='flagged-posts'),    
    url(r'^staff/$', views.staff, name='staff'), 
    url(r'^update-staff/(?P<user>[A-Za-z0-9]+)', views.updateStaffStatus, name='update-staff'),
    url(r'^update-active/(?P<user>[A-Za-z0-9]+)', views.updateActiveStatus, name='update-active'),

    # url: /posts/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url: /posts/topics/
    url(r'^topics/$', views.TopicsView.as_view(), name='topics'),
    # url: /posts/topics/Education
    url(r'^topics/(?P<topic>[A-Za-z]+)', views.PostsWithSameTopicView.as_view(), name='topic'),
    
    # any other page will load a 'page not found'. this should always be the last url
    # url(r'^', views.pageNotFound, name='page-not-found'), 

]

