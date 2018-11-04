from django.db import models

# Create your models here.
class Post(models.Model):
    postedBy = models.CharField(max_length=30)
    postTitle = models.CharField(max_length=80)
    postTopic = models.CharField(max_length=30)
    postContent = models.TextField()
    postDate = models.DateTimeField()
    postNumberOfLikes = models.IntegerField()
    postNumberOfVotes = models.IntegerField()
    postNumberOfFlags = models.IntegerField()
    postNumberOfComments = models.IntegerField()

    def __str__(self):
        return "Post " + str(self.pk) 
    
class Comment(models.Model):
    commentOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentContent = models.TextField()
    commentBy = models.CharField(max_length=30)
    commentDate = models.DateTimeField()
    commentNumberOfLikes = models.IntegerField()
    commentNumberOfVotes = models.IntegerField()
    commentNumberOfFlags = models.IntegerField()

    def __str__(self):
        return "Comment " + str(self.pk) + " on " + str(self.commentOnPost)
    
class Reply(models.Model):
    replytoComment = models.ForeignKey(Comment ,on_delete=models.CASCADE)
    replyContent = models.TextField()
    replyBy = models.CharField(max_length=30)
    replyDate = models.DateTimeField()
    replyNumberOfLikes = models.IntegerField()
    replyNumberOfFlags = models.IntegerField()

    def __str__(self):
        return "Reply " + str(self.pk) + " to " + str(self.replytoComment)
    
