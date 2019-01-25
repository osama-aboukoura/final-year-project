from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_of_posts_comments_replies = models.IntegerField(default=0)
    num_of_likes = models.IntegerField(default=0)
    activation_code = models.CharField(max_length=30)
    reset_password_code = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username 
