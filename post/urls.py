from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    # url looks like: /post/ 
    url(r'^$', views.index, name='index'),
    
    # url looks like: /post/4/
    url(r'^(?P<post_id>[0-9]+)/$', views.showPost, name='showPost'),
]

