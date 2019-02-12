from django.conf.urls import url
from . import views

app_name = 'comment'

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/add-comment/$', views.Comment_Create.as_view(), name='add-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/edit-comment/$', views.Comment_Update.as_view(), name='edit-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/delete-comment/$', views.Comment_Delete.as_view(), name='delete-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-like/$', views.Comment_Like.as_view(), name='like-comment'),
    url(r'^(?P<pk>[0-9]+)/comment-likes-list/$', views.Comment_Likes_List.as_view(), name='like-list-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-vote-up/$', views.Comment_Vote_Up.as_view(), name='vote-up-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/comment-vote-down/$', views.Comment_Vote_Down.as_view(), name='vote-down-comment'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/report-comment/$', views.Comment_Report.as_view(), name='report-comment'),
    url(r'^(?P<pk>[0-9]+)/disable-comment/$', views.Comment_Enable_Disable_Page.as_view(), name='disable-comment'),
    url(r'^(?P<pk>[0-9]+)/disable-comment-confirm/$', views.Comment_Enable_Disable.as_view(), name='disable-comment-confirm'),
    url(r'^(?P<pk>[0-9]+)/remove-comment-flags/$', views.Comment_Remove_Flags_Page.as_view(), name='remove-comment-flags'),
    url(r'^(?P<pk>[0-9]+)/remove-comment-flags-confirm/$', views.Comment_Remove_Flags.as_view(), name='remove-comment-flags-confirm'),
    url(r'^(?P<post_pk>[0-9]+)/(?P<pk>[0-9]+)/accept-answer/$', views.Accept_Answer.as_view(), name='accept-answer'),
]

