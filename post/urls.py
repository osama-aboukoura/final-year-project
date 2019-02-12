from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.Show_Post_View.as_view(), name='show-post'),
    url(r'^add-post/$', views.Post_Create.as_view(), name='add-post'),
    url(r'^(?P<pk>[0-9]+)/edit-post/$', views.Post_Update.as_view(), name='edit-post'),
    url(r'^(?P<pk>[0-9]+)/delete-post/$', views.Post_Delete.as_view(), name='delete-post'),
    url(r'^(?P<pk>[0-9]+)/like/$', views.Post_Like.as_view(), name='like-post'),
    url(r'^(?P<pk>[0-9]+)/post-likes-list/$', views.Post_Likes_List.as_view(), name='like-list-post'),
    url(r'^(?P<pk>[0-9]+)/post-vote-up/$', views.Post_Vote_Up.as_view(), name='vote-up-post'),
    url(r'^(?P<pk>[0-9]+)/post-vote-down/$', views.Post_Vote_Down.as_view(), name='vote-down-post'),
    url(r'^(?P<pk>[0-9]+)/report-post/$', views.Post_Report.as_view(), name='report-post'),
    url(r'^(?P<pk>[0-9]+)/disable-post/$', views.Post_Enable_Disable_Page.as_view(), name='disable-post'),
    url(r'^(?P<pk>[0-9]+)/disable-post-confirm/$', views.Post_Enable_Disable.as_view(), name='disable-post-confirm'),
    url(r'^(?P<pk>[0-9]+)/remove-post-flags/$', views.Post_Remove_Flags_Page.as_view(), name='remove-post-flags'),
    url(r'^(?P<pk>[0-9]+)/remove-post-flags-confirm/$', views.Post_Remove_Flags.as_view(), name='remove-post-flags-confirm'),
    url(r'^(?P<pk>[0-9]+)/open-comments/$', views.Post_Open_Comments.as_view(), name='open-comments'),
      
]

