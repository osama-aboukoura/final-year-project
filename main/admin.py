from django.contrib import admin
from .models import UserProfile

# this class is to customise what the admin would see on the admin panel 
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "__str__"]
    list_display_links = ["__str__"]
    class Meta:
        model = UserProfile 

# adding the UserProfile model to the admin panel
admin.site.register(UserProfile, UserProfileModelAdmin)
