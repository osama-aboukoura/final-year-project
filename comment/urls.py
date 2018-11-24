from django.conf.urls import url
from . import views

app_name = 'comment'

urlpatterns = [

    # url: /posts/3/add-comment/
    url(r'^(?P<pk>[0-9]+)/add-comment/$', views.CommentCreate.as_view(), name='add-comment'),
    # url: /posts/3/2/edit-comment/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/edit-comment/$', views.CommentUpdate.as_view(), name='edit-comment'),
    # url: /posts/3/2/delete-comment/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/delete-comment/$', views.CommentDelete.as_view(), name='delete-comment'),
    # url: /posts/3/2/comment-like/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-like/$', views.CommentLike.as_view(), name='like-comment'),
    # url: /posts/3/2/comment-vote-up/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-vote-up/$', views.CommentVoteUp.as_view(), name='vote-up-comment'),
    # url: /posts/3/2/comment-vote-down/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-vote-down/$', views.CommentVoteDown.as_view(), name='vote-down-comment'),
    # url: /posts/3/2/report-comment/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/report-comment/$', views.CommentReport.as_view(), name='report-comment'),
    # url: /posts/3/2/disable-comment/
    url(r'^(?P<pk>[0-9]+)/disable-comment/$', views.CommentEnableDisablePage.as_view(), name='disable-comment'),
    # url: /posts/3/disable-comment-confirm/
    url(r'^(?P<pk>[0-9]+)/disable-comment-confirm/$', views.CommentEnableDisable.as_view(), name='disable-comment-confirm'),
    # url: /posts/3/remove-comment-flags/
    url(r'^(?P<pk>[0-9]+)/remove-comment-flags/$', views.CommentRemoveFlagsPage.as_view(), name='remove-comment-flags'),
    # url: /posts/3/remove-comment-flags/
    url(r'^(?P<pk>[0-9]+)/remove-comment-flags-confirm/$', views.CommentRemoveFlags.as_view(), name='remove-comment-flags-confirm'),
 
]

