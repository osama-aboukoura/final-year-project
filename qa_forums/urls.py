from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('post.urls')),
    url(r'^', include('comment.urls')),
    url(r'^', include('reply.urls')),
    url(r'^', include('main.urls')),
] 

# urls for any images uploaded by user
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
