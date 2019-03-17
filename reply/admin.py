from django.contrib import admin
from .models import Reply

# this class is to customise what the admin would see on the admin panel 
class ReplyModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__", "replyBy", "replyDate"]
    list_display_links = ["__str__"]
    search_fields = ["replyContent", "replyBy"]
    list_filter = ["replyDate"]
    class Meta:
        model = Reply 

# adding the Reply model to the admin panel
admin.site.register(Reply, ReplyModelAdmin)
