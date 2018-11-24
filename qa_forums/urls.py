from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('post.urls')),
    url(r'^', include('comment.urls')),
    url(r'^', include('reply.urls')),
    url(r'^', include('main.urls')),
]
