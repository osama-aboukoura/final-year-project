from django.contrib import admin
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "commentBy", "commentDate"]
    list_display_links = ["__str__"]
    search_fields = ["commentContent", "commentBy"]
    list_filter = ["commentDate"]
    class Meta:
        model = Comment

admin.site.register(Comment, CommentModelAdmin)
