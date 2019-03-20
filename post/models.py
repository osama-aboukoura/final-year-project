from django.db import models
from django.urls import reverse
from main.models import UserProfile

# a model for storing a post in the database 
class Post(models.Model):
    postedBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    postTitle = models.CharField(max_length=80, verbose_name=('Post Title'))
    postTopic = models.CharField(max_length=60, verbose_name=('Post Topic'), blank=True)
    postTopicRelatedWords = models.TextField(max_length=150, blank=True)
    postContent = models.TextField(max_length=350, verbose_name=('Post'))
    postImage = models.ImageField(null=True, blank=True)
    postLastUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)
    postDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    postLikes = models.ManyToManyField(UserProfile, blank=True, related_name='post_likes')
    postNumberOfVotes = models.IntegerField(default=0)
    postVotersUp = models.ManyToManyField(UserProfile, blank=True, related_name='post_votes_up')
    postVotersDown = models.ManyToManyField(UserProfile, blank=True, related_name='post_votes_down')
    postNumberOfComments = models.IntegerField(default=0)
    postFlags = models.ManyToManyField(UserProfile, blank=True, related_name='post_flags')
    postDisabled = models.BooleanField(default=False)
    postClosed = models.BooleanField(default=False)
    postAutoClassification = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("post:show-post", kwargs={"pk": self.pk})
    
    # a string representation of the object stored 
    def __str__(self):
        return "Post " + str(self.pk) 
    
    # list posts in a descending order according to the number of votes then the post date 
    class Meta:
        ordering=["-postNumberOfVotes", "-postDate"]

