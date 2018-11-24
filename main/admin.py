from django.contrib import admin
from .models import UserProfile

class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
    list_display_links = ["__str__"]
    class Meta:
        model = UserProfile 

admin.site.register(UserProfile, UserProfileModelAdmin)
