from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    # url looks like: /post/ 
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # url looks like: /post/4/
    url(r'^(?P<pk>[0-9]+)/$', views.ShowPostView.as_view(), name='showPost'),

    url(r'^addpost/$', views.PostCreate.as_view(), name='post-add'),

    url(r'^(?P<pk>[0-9]+)/addcomment/$', views.CommentCreate.as_view(), name='comment-add'),

    url(r'^(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/addreply/$', views.ReplyCreate.as_view(), name='reply-add'),
]

