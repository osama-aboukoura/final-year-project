from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length=80)
    postTopic = models.CharField(max_length=30)
    postContent = models.TextField()
    postImage = models.ImageField(null=True, blank=True)
    postDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    postLikes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    postNumberOfVotes = models.IntegerField(default=0)
    postVotersUp = models.ManyToManyField(User, blank=True, related_name='post_votes_up')
    postVotersDown = models.ManyToManyField(User, blank=True, related_name='post_votes_down')
    postNumberOfFlags = models.IntegerField(default=0)
    postNumberOfComments = models.IntegerField(default=0)
    postFlags = models.ManyToManyField(User, blank=True, related_name='post_flags')
    postDisabled = models.BooleanField(default=False)

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
    commentImage = models.ImageField(null=True, blank=True)
    commentDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    commentLikes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    commentNumberOfVotes = models.IntegerField(default=0)
    commentVotersUp = models.ManyToManyField(User, blank=True, related_name='comment_votes_up')
    commentVotersDown = models.ManyToManyField(User, blank=True, related_name='comment_votes_down')
    commentFlags = models.ManyToManyField(User, blank=True, related_name='comment_flags')
    commentDisabled = models.BooleanField(default=False)

    def __str__(self):
        return "Comment " + str(self.pk) + " on " + str(self.commentOnPost)

    class Meta:
        ordering=["-commentNumberOfVotes"]
    