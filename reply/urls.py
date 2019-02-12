from django.conf.urls import url
from . import views

app_name = 'reply'

urlpatterns = [

    url(r'^(?P<post_pk>[0-9]+)/(?P<comment_pk>[0-9]+)/add-reply/$', views.Reply_Create.as_view(), name='add-reply'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/edit-reply/$', views.Reply_Update.as_view(), name='edit-reply'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/delete-reply/$', views.Reply_Delete.as_view(), name='delete-reply'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/reply-like/$', views.Reply_Like.as_view(), name='like-reply'),
    url(r'^(?P<pk>[0-9]+)/reply-likes-list/$', views.Reply_Likes_List.as_view(), name='like-list-reply'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/report-reply/$', views.Reply_Report.as_view(), name='report-reply'),
    url(r'^(?P<pk>[0-9]+)/disable-reply/$', views.Reply_Enable_Disable_Page.as_view(), name='disable-reply'),
    url(r'^(?P<pk>[0-9]+)/disable-reply-confirm/$', views.Reply_Enable_Disable.as_view(), name='disable-reply-confirm'),
    url(r'^(?P<pk>[0-9]+)/remove-reply-flags/$', views.Reply_Remove_Flags_Page.as_view(), name='remove-reply-flags'),
    url(r'^(?P<pk>[0-9]+)/remove-reply-flags-confirm/$', views.Reply_Remove_Flags.as_view(), name='remove-reply-flags-confirm'),
    
]

