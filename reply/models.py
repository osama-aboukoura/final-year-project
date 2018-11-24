from django.db import models
from django.contrib.auth.models import User
from comment.models import Comment

class Reply(models.Model):
    replytoComment = models.ForeignKey(Comment ,on_delete=models.CASCADE)
    replyContent = models.TextField()
    replyBy = models.ForeignKey(User, on_delete=models.CASCADE)
    replyDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    replyLikes = models.ManyToManyField(User, blank=True, related_name='reply_likes')
    replyFlags = models.ManyToManyField(User, blank=True, related_name='reply_flags')
    replyDisabled = models.BooleanField(default=False)

    def __str__(self):
        return "Reply " + str(self.pk) + " to " + str(self.replytoComment)
    
