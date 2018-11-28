from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<user>[A-Za-z0-9]+)$', views.profileInfo, name='profile'),    
    url(r'^flagged-posts/$', views.flaggedPostsView, name='flagged-posts'),    

    # url: /posts/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url: /posts/topics/
    url(r'^topics/$', views.TopicsView.as_view(), name='topics'),
    # url: /posts/topics/Education
    url(r'^topics/(?P<topic>[A-Za-z]+)', views.PostsWithSameTopicView.as_view(), name='topic'),
  
]

