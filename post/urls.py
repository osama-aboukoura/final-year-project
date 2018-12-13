from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.ShowPostView.as_view(), name='showPost'),
    url(r'^add-post/$', views.PostCreate.as_view(), name='add-post'),
    url(r'^(?P<pk>[0-9]+)/edit-post/$', views.PostUpdate.as_view(), name='edit-post'),
    url(r'^(?P<pk>[0-9]+)/delete-post/$', views.PostDelete.as_view(), name='delete-post'),
    url(r'^(?P<pk>[0-9]+)/like/$', views.PostLike.as_view(), name='like-post'),
    url(r'^(?P<pk>[0-9]+)/post-likes-list/$', views.PostLikesList.as_view(), name='like-list-post'),
    url(r'^(?P<pk>[0-9]+)/post-vote-up/$', views.PostVoteUp.as_view(), name='vote-up-post'),
    url(r'^(?P<pk>[0-9]+)/post-vote-down/$', views.PostVoteDown.as_view(), name='vote-down-post'),
    url(r'^(?P<pk>[0-9]+)/report-post/$', views.PostReport.as_view(), name='report-post'),
    url(r'^(?P<pk>[0-9]+)/disable-post/$', views.PostEnableDisablePage.as_view(), name='disable-post'),
    url(r'^(?P<pk>[0-9]+)/disable-post-confirm/$', views.PostEnableDisable.as_view(), name='disable-post-confirm'),
    url(r'^(?P<pk>[0-9]+)/remove-post-flags/$', views.PostRemoveFlagsPage.as_view(), name='remove-post-flags'),
    url(r'^(?P<pk>[0-9]+)/remove-post-flags-confirm/$', views.PostRemoveFlags.as_view(), name='remove-post-flags-confirm'),
    url(r'^(?P<pk>[0-9]+)/open-comments/$', views.PostOpenComments.as_view(), name='open-comments'),
      
]

