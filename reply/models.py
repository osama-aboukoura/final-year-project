from django.db import models
from main.models import UserProfile
from comment.models import Comment

# a model for storing a reply in the database 
class Reply(models.Model):
    replytoComment = models.ForeignKey(Comment ,on_delete=models.CASCADE)
    replyContent = models.TextField(max_length=350, verbose_name=('Reply to Comment:'))
    replyBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    replyDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    replyLikes = models.ManyToManyField(UserProfile, blank=True, related_name='reply_likes')
    replyFlags = models.ManyToManyField(UserProfile, blank=True, related_name='reply_flags')
    replyDisabled = models.BooleanField(default=False)

    # a string representation of the object stored 
    def __str__(self):
        return "Reply " + str(self.pk) + " to " + str(self.replytoComment)
    
