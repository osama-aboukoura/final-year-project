from django.conf.urls import url
from . import views

urlpatterns = [
    # url looks like: / 
    url(r'^$', views.index, name='index'),    
]

