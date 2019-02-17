from django.test import TestCase
from post.models import Post
from comment.models import Comment
from main.models import User, UserProfile

class TestModels(TestCase):
    def set_up(self):
        self.user = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
        self.user.set_password('password123')
        self.user.save() 
        self.userProfile = UserProfile.objects.create ( pk = '1', user = self.user)
        
        self.post = Post.objects.create(
            postedBy = self.userProfile,
            postTitle = 'Holiday in Istanbul?',
            postTopic = 'Travel',
            postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
        )

        self.comment = Comment.objects.create(
            commentOnPost = self.post,
            commentBy = self.userProfile, 
            commentContent = 'They have special deals towards the end of the summer.'
        )

    def test_comment_given_a_unique_id_1_on_creation(self):
        self.set_up()
        self.assertEquals(self.comment.pk, 1) # the first id given is 1 then it auto increments
    
    def test_comment_given_a_unique_id_2_on_creation(self):
        self.set_up()
        comment = Comment.objects.create(
            commentOnPost = self.post,
            commentBy = self.userProfile,
            commentContent = 'Their cheapest deals are in the winter'
        )
        comment.save()
        self.assertEquals(comment.pk, 2) # the first id given is 1 then it auto increments
    
    def test_comment_string_representation(self):
        self.set_up()
        self.assertEquals(str(self.comment), "Comment 1 on Post 1") 