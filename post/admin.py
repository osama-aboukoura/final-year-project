from django.contrib import admin
from .models import Post, UserProfile

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "postTitle", "postTopic", "postedBy", "postDate"]
    list_display_links = ["postTitle"]
    search_fields = ["postTitle", "postTopic", "postContent", "postedBy"]
    list_filter = ["postDate"]
    class Meta:
        model = Post

class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
    list_display_links = ["__str__"]
    class Meta:
        model = UserProfile 

admin.site.register(Post, PostModelAdmin)

admin.site.register(UserProfile, UserProfileModelAdmin)

