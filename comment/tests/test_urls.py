from django.test import TestCase, Client
from django.urls import reverse, resolve
from post.models import Post
from comment.models import Comment
from comment.views import *

class TestCommentUrls(TestCase):
    # a set up function that gets called in other functions 
    # creates a user, a userProfile, a post and a comment
    def set_up(self):
        self.client = Client()
        self.user = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
        self.userProfile = UserProfile.objects.create (user = self.user)
        self.post = Post.objects.create(
            postedBy = self.userProfile,
            postTitle = 'Holiday in Istanbul?',
            postTopic = 'Travel',
            postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
        )
        self.comment = Comment.objects.create(
            commentOnPost = self.post,
            commentBy = self.userProfile, # ideally a different user would be adding this comment
            commentContent = 'They have special deals towards the end of the summer.'
        )


    # the following tests check if each url resolves correctly 
    # and calls the right function in the views 
    
    def test_add_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:add-comment', kwargs={'pk': self.post.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Create)
    
    def test_edit_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:edit-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Update)
    
    def test_delete_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:delete-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Delete)
    
    def test_like_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:like-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Like)
    
    def test_likes_list_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:like-list-comment', kwargs={'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Likes_List)
    
    def test_vote_up_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:vote-up-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Vote_Up)
    
    def test_vote_down_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:vote-down-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Vote_Down)
    
    def test_report_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:report-comment', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Report)
    
    def test_disable_enable_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:disable-comment', kwargs={'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Enable_Disable_Page)
    
    def test_disable_enable_confirm_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:disable-comment-confirm', kwargs={'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Enable_Disable)
    
    def test_remove_flags_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:remove-comment-flags', kwargs={'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Remove_Flags_Page)
    
    def test_remove_flags_confirm_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:remove-comment-flags-confirm', kwargs={'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Comment_Remove_Flags)

    def test_accept_answer_comment_url_resolves(self):
        self.set_up()
        url = reverse('comment:accept-answer', kwargs={'post_pk': self.post.pk, 'pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Accept_Answer)
    