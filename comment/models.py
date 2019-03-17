from django.db import models
from post.models import Post
from main.models import UserProfile

# a model for storing a comment in the database 
class Comment(models.Model):
    commentOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentContent = models.TextField(max_length=350, verbose_name=('Comment on Post:'))
    commentBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    commentImage = models.ImageField(null=True, blank=True)
    commentDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    commentLikes = models.ManyToManyField(UserProfile, blank=True, related_name='comment_likes')
    commentNumberOfVotes = models.IntegerField(default=0)
    commentVotersUp = models.ManyToManyField(UserProfile, blank=True, related_name='comment_votes_up')
    commentVotersDown = models.ManyToManyField(UserProfile, blank=True, related_name='comment_votes_down')
    commentFlags = models.ManyToManyField(UserProfile, blank=True, related_name='comment_flags')
    commentDisabled = models.BooleanField(default=False)
    commentAccepted = models.BooleanField(default=False)

    # a string representation of the object stored 
    def __str__(self):
        return "Comment " + str(self.pk) + " on " + str(self.commentOnPost)

    # list comments in a descending order according to the number of votes
    class Meta:
        ordering=["-commentNumberOfVotes"]
