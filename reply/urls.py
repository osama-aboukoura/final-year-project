from django.conf.urls import url
from . import views

app_name = 'reply'

urlpatterns = [

    # url: /posts/2/4/add-reply/
    url(r'^(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/add-reply/$', views.ReplyCreate.as_view(), name='add-reply'),
    # url: /posts/3/2/edit-reply/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/edit-reply/$', views.ReplyUpdate.as_view(), name='edit-reply'),
    # url: /posts/3/2/delete-reply/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/delete-reply/$', views.ReplyDelete.as_view(), name='delete-reply'),
    # url: /posts/3/2/reply-like/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/reply-like/$', views.ReplyLike.as_view(), name='like-reply'),
    # url: /posts/3/2/report-reply/
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/report-reply/$', views.ReplyReport.as_view(), name='report-reply'),
    # url: /posts/3/2/disable-reply/
    url(r'^(?P<pk>[0-9]+)/disable-reply/$', views.ReplyEnableDisablePage.as_view(), name='disable-reply'),
    # url: /posts/3/2/disable-reply-confirm/
    url(r'^(?P<pk>[0-9]+)/disable-reply-confirm/$', views.ReplyEnableDisable.as_view(), name='disable-reply-confirm'),
    # url: /posts/3/remove-reply-flags/
    url(r'^(?P<pk>[0-9]+)/remove-reply-flags/$', views.ReplyRemoveFlagsPage.as_view(), name='remove-reply-flags'),
    # url: /posts/3/remove-reply-flags/
    url(r'^(?P<pk>[0-9]+)/remove-reply-flags-confirm/$', views.ReplyRemoveFlags.as_view(), name='remove-reply-flags-confirm'),
    
]

