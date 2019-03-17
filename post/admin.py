from django.contrib import admin
from .models import Post

# this class is to customise what the admin would see on the admin panel 
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "postTitle", "postTopic", "postedBy", "postDate"]
    list_display_links = ["postTitle"]
    search_fields = ["postTitle", "postTopic", "postContent", "postedBy"]
    list_filter = ["postDate"]
    class Meta:
        model = Post

# adding the Post model to the admin panel
admin.site.register(Post, PostModelAdmin)


