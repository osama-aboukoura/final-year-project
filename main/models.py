from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numOfPostsCommentsReplies = models.IntegerField(default=0)
    numberOfLikes = models.IntegerField(default=0)
    activationCode = models.CharField(max_length=30, blank=True)
    resetPasswordCode = models.CharField(max_length=30, blank=True)
    dateJoined = models.DateTimeField(auto_now=False, auto_now_add=True)
    profilePicture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username
