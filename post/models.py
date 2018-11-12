from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    # postedBy = models.CharField(max_length=30)
    postTitle = models.CharField(max_length=80)
    postTopic = models.CharField(max_length=30)
    postContent = models.TextField()
    postImage = models.ImageField(null=True, blank=True)
    postDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    postNumberOfLikes = models.IntegerField(default=0)
    postNumberOfVotes = models.IntegerField(default=0)
    postNumberOfFlags = models.IntegerField(default=0)
    postNumberOfComments = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post:showPost", kwargs={"pk": self.pk})
    
    def __str__(self):
        return "Post " + str(self.pk) 
    
    class Meta:
        ordering=["-postNumberOfVotes", "-postDate"]


class Comment(models.Model):
    commentOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentContent = models.TextField()
    commentBy = models.ForeignKey(User, on_delete=models.CASCADE)
    # commentBy = models.CharField(max_length=30)
    commentImage = models.ImageField(null=True, blank=True)
    commentDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    commentNumberOfLikes = models.IntegerField(default=0)
    commentNumberOfVotes = models.IntegerField(default=0)
    commentNumberOfFlags = models.IntegerField(default=0)

    def __str__(self):
        return "Comment " + str(self.pk) + " on " + str(self.commentOnPost)

    class Meta:
        ordering=["-commentNumberOfVotes"]
    
class Reply(models.Model):
    replytoComment = models.ForeignKey(Comment ,on_delete=models.CASCADE)
    replyContent = models.TextField()
    replyBy = models.ForeignKey(User, on_delete=models.CASCADE)
    # replyBy = models.CharField(max_length=30)
    replyDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    replyNumberOfLikes = models.IntegerField(default=0)
    replyNumberOfFlags = models.IntegerField(default=0)

    def __str__(self):
        return "Reply " + str(self.pk) + " to " + str(self.replytoComment)
    
