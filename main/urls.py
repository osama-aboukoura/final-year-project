from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user-login'),
    url(r'^logout/$', views.user_logout, name='user-logout'),
    url(r'^activate/$', views.activate, name='activate'),
    url(r'^resend-username/$', views.resend_username, name='resend-username'),
    url(r'^reset-password/$', views.reset_password, name='reset-password'),
    url(r'^reset-password-auth/$', views.reset_password_auth, name='reset-password-auth'),
    url(r'^reset-password-confirm/$', views.reset_password_confirm, name='reset-password-confirm'),
    url(r'^profile/(?P<user>[A-Za-z0-9]+)$', views.profile_info, name='profile'),    
    url(r'^edit-profile/(?P<user>[A-Za-z0-9]+)$', views.edit_profile_info, name='edit-profile'),    
    url(r'^delete-profile/$', views.delete_profile_and_user, name='delete-profile'),    
    url(r'^delete-profile-confirm/$', views.delete_profile_and_user_confirm, name='delete-profile-confirm'),    
    url(r'^flagged-posts/$', views.flagged_posts_view, name='flagged-posts'),    
    url(r'^staff/$', views.staff, name='staff'), 
    url(r'^update-staff/(?P<user>[A-Za-z0-9]+)', views.update_staff_status, name='update-staff'),
    url(r'^update-active/(?P<user>[A-Za-z0-9]+)', views.update_active_status, name='update-active'),

    # links for class-based views 
    url(r'^$', views.Index_View.as_view(), name='index'),
    url(r'^topics/$', views.Topics_View.as_view(), name='topics'),
    url(r'^topics/(?P<topic>[A-Za-z]+)', views.Posts_With_Same_Topic_View.as_view(), name='topic'),
    
    url(r'^page-not-found/', views.pageNotFound, name='page-not-found'), 

]

