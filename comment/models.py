from django.db import models
from django.contrib.auth.models import User
from post.models import Post

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
