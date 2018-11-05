from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    # url: /posts/ 
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url: /posts/4/
    url(r'^(?P<pk>[0-9]+)/$', views.ShowPostView.as_view(), name='showPost'),

    # url: /add-post/
    url(r'^add-post/$', views.PostCreate.as_view(), name='add-post'),
    # url: /posts/3/add-comment/
    url(r'^(?P<pk>[0-9]+)/add-comment/$', views.CommentCreate.as_view(), name='add-comment'),
    # url: /posts/2/4/add-reply/
    url(r'^(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/add-reply/$', views.ReplyCreate.as_view(), name='add-reply'),

    # url: /posts/3/edit-post/
    url(r'^(?P<pk>[0-9]+)/edit-post/$', views.PostUpdate.as_view(), name='edit-post'),
    # url: /posts/3/delete-post/
    url(r'^(?P<pk>[0-9]+)/delete-post/$', views.PostDelete.as_view(), name='delete-post'),

]

