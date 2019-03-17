from django.contrib import admin
from .models import Comment

# this class is to customise what the admin would see on the admin panel 
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "commentBy", "commentDate"]
    list_display_links = ["__str__"]
    search_fields = ["commentContent", "commentBy"]
    list_filter = ["commentDate"]
    class Meta:
        model = Comment

# adding the Comment model to the admin panel
admin.site.register(Comment, CommentModelAdmin)
