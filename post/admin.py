from django.contrib import admin
from .models import Post, Comment, Reply, UserProfile

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "postTitle", "postTopic", "postedBy", "postDate"]
    list_display_links = ["postTitle"]
    search_fields = ["postTitle", "postTopic", "postContent", "postedBy"]
    list_filter = ["postDate"]
    class Meta:
        model = Post

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "commentBy", "commentDate"]
    list_display_links = ["__str__"]
    search_fields = ["commentContent", "commentBy"]
    list_filter = ["commentDate"]
    class Meta:
        model = Comment

class ReplyModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "replyBy", "replyDate"]
    list_display_links = ["__str__"]
    search_fields = ["replyContent", "replyBy"]
    list_filter = ["replyDate"]
    class Meta:
        model = Reply 

admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Reply, ReplyModelAdmin)

admin.site.register(UserProfile)

