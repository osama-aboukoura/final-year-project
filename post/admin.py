from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "postTitle", "postTopic", "postedBy", "postDate"]
    list_display_links = ["postTitle"]
    search_fields = ["postTitle", "postTopic", "postContent", "postedBy"]
    list_filter = ["postDate"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)


