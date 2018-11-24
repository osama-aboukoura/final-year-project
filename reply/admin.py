from django.contrib import admin
from .models import Reply

# Register your models here.
class ReplyModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "replyBy", "replyDate"]
    list_display_links = ["__str__"]
    search_fields = ["replyContent", "replyBy"]
    list_filter = ["replyDate"]
    class Meta:
        model = Reply 

admin.site.register(Reply, ReplyModelAdmin)
