from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<user>[A-Za-z0-9]+)$', views.profileInfo, name='profile'),    
    url(r'^flagged-posts/$', views.FlaggedPostsView.as_view(), name='flagged-posts'),    

    # url: /posts/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url: /posts/topics/
    url(r'^topics/$', views.TopicsView.as_view(), name='topics'),
    # url: /posts/topics/Education
    url(r'^topics/(?P<topic>[A-Za-z]+)', views.PostsWithSameTopicView.as_view(), name='topic'),

    # url: /posts/4/
    url(r'^(?P<pk>[0-9]+)/$', views.ShowPostView.as_view(), name='showPost'),

    # url: /posts/add-post/
    url(r'^add-post/$', views.PostCreate.as_view(), name='add-post'),
    # url: /posts/3/edit-post/
    url(r'^(?P<pk>[0-9]+)/edit-post/$', views.PostUpdate.as_view(), name='edit-post'),
    # url: /posts/3/delete-post/
    url(r'^(?P<pk>[0-9]+)/delete-post/$', views.PostDelete.as_view(), name='delete-post'),
    # url: /posts/3/like/
    url(r'^(?P<pk>[0-9]+)/like/$', views.PostLike.as_view(), name='like-post'),
    # url: /posts/3/post-vote-up/
    url(r'^(?P<pk>[0-9]+)/post-vote-up/$', views.PostVoteUp.as_view(), name='vote-up-post'),
    # url: /posts/3/post-vote-down/
    url(r'^(?P<pk>[0-9]+)/post-vote-down/$', views.PostVoteDown.as_view(), name='vote-down-post'),
    # url: /posts/3/report-post/
    url(r'^(?P<pk>[0-9]+)/report-post/$', views.PostReport.as_view(), name='report-post'),
    # url: /posts/3/disable-post/
    url(r'^(?P<pk>[0-9]+)/disable-post/$', views.PostEnableDisablePage.as_view(), name='disable-post'),
    # url: /posts/3/disable-post-confirm/
    url(r'^(?P<pk>[0-9]+)/disable-post-confirm/$', views.PostEnableDisable.as_view(), name='disable-post-confirm'),
    # url: /posts/3/remove-post-flags/
    url(r'^(?P<pk>[0-9]+)/remove-post-flags/$', views.PostRemoveFlagsPage.as_view(), name='remove-post-flags'),
    # url: /posts/3/remove-post-flags/
    url(r'^(?P<pk>[0-9]+)/remove-post-flags-confirm/$', views.PostRemoveFlags.as_view(), name='remove-post-flags-confirm'),
      
]

