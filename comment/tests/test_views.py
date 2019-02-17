from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, UserProfile
from post.models import Post
from comment.models import Comment
from django.contrib.auth import authenticate, login
import json

class TestViews(TestCase):

    def set_up(self):
        self.client = Client()

        self.user = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
        self.user.set_password('password123')
        self.user.save()
        self.userProfile = UserProfile.objects.create (user = self.user)

        self.user2 = User.objects.create(username = 'user2', email = 'osama@kcl.ac.uk')
        self.user2.set_password('password123')
        self.user2.save()
        self.userProfile2 = UserProfile.objects.create (user = self.user2)

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

        self.comment2 = Comment.objects.create(
            commentOnPost = self.post,
            commentBy = self.userProfile2, 
            commentContent = 'Their cheapest deals are in the winter'
        )

        self.client.login(username='osamaaboukoura', password='password123') 

    def test_add_comment_GET_view(self):
        self.set_up()
        response = self.client.get(reverse('comment:add-comment', args=['1']))
        self.assertTemplateUsed(response, 'comment/comment_form.html')
    
    def test_add_comment_POST_view(self):
        self.set_up()
        response = self.client.post(reverse('comment:add-comment', args=['1']), {
            'commentBy': self.userProfile,
            'commentContent': 'Not very expensive'
        })
        comment = Comment.objects.get(pk=3)
        self.assertEquals(comment.commentContent, 'Not very expensive') 
        self.assertEquals(response.status_code, 302) # redirect status code
        
    def test_delete_comment_view(self):
        self.set_up()
        response = self.client.delete(reverse('comment:delete-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }), json.dumps({
            'id': 1
        }))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Comment.objects.count(), 1) # one comment left after deletion 
    
    def test_update_comment_GET_view(self):
        self.set_up()
        response = self.client.get(reverse('comment:edit-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.assertTemplateUsed(response, "comment/comment_edit_form.html")
    
    def test_update_comment_POST_view(self):
        self.set_up()
        self.client.post(reverse('comment:edit-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }), {
            'commentContent': 'IT IS VERY EXPENSIVE!'
        })
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentContent, 'IT IS VERY EXPENSIVE!') 

    def test_comment_like(self):
        self.set_up()
        # adding a like 
        self.client.get(reverse('comment:like-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.assertEquals(self.comment.commentLikes.count(), 1) # comment has 1 like now
        # list of users who liked the comment
        response = self.client.get(reverse('comment:like-list-comment', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, "comment/comment-likes-list.html")
        # removing a like 
        self.client.get(reverse('comment:like-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.assertEquals(self.comment.commentLikes.count(), 0) # comment has 0 likes now

    def test_comment_vote_up(self):
        self.set_up()
        # adding a vote up
        self.client.get(reverse('comment:vote-up-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentVotersUp.count(), 1) # comment has 1 vote up now
        self.assertEquals(self.comment.commentNumberOfVotes, 1) 
        # removing a vote up
        self.client.get(reverse('comment:vote-up-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentVotersUp.count(), 0) # comment has 1 vote up now
        self.assertEquals(self.comment.commentNumberOfVotes, 0) 
    
    def test_comment_vote_down(self):
        self.set_up()
        # adding a vote down
        self.client.get(reverse('comment:vote-down-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentVotersDown.count(), 1) # comment has 1 vote down now
        self.assertEquals(self.comment.commentNumberOfVotes, -1) 
        # removing a vote down
        self.client.get(reverse('comment:vote-down-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentVotersDown.count(), 0) # comment has 0 vote down now
        self.assertEquals(self.comment.commentNumberOfVotes, 0) 
        
    def test_comment_report(self):
        self.set_up()
        self.client.get(reverse('comment:report-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentFlags.count(), 1)

    def test_comment_disable_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('comment:disable-comment', kwargs={'pk': self.comment.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-comment.html") # not used because user isn't staff

    def test_comment_disable_page_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('comment:disable-comment', kwargs={'pk': self.comment.pk}))
        self.assertTemplateUsed(response, "main/flagged-posts/disable-comment.html")
    
    def test_comment_disable_confirm_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('comment:disable-comment-confirm', kwargs={'pk': self.comment.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-comment-confirm.html") 
    
    def test_comment_disable_confirm_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        self.client.get(reverse('comment:disable-comment-confirm', kwargs={'pk': self.comment.pk}))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentDisabled, True)

    def test_comment_remove_flags_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('comment:remove-comment-flags', kwargs={'pk': self.comment.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/remove-flags-comment.html") # not used because user isn't staff

    def test_comment_remove_flags_page_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('comment:remove-comment-flags', kwargs={'pk': self.comment.pk}))
        self.assertTemplateUsed(response, "main/flagged-posts/remove-flags-comment.html")
    
    def test_comment_remove_flags_confirm_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('comment:remove-comment-flags-confirm', kwargs={'pk': self.comment.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-comment-confirm.html") 
    
    def test_comment_remove_flags_confirm_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        self.client.get(reverse('comment:report-comment', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentFlags.count(), 1)
        self.client.get(reverse('comment:remove-comment-flags-confirm', kwargs={'pk': self.comment.pk}))
        self.comment.refresh_from_db()
        self.assertEquals(self.comment.commentFlags.count(), 0)

    def test_post_owner_can_accept_comments_by_another_user(self):
        self.set_up()
        self.client.get(reverse('comment:accept-answer', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment2.pk
        }))
        self.comment2.refresh_from_db()
        self.assertTrue(self.comment2.commentAccepted) # assert TRUE because they can accpet.
    
    def test_post_owner_cannot_accept_comments_they_made_themselves(self):
        self.set_up()
        self.client.get(reverse('comment:accept-answer', kwargs={
            'post_pk': self.post.pk, 'pk': self.comment.pk
        }))
        self.comment.refresh_from_db()
        self.assertFalse(self.comment.commentAccepted) # assert FALSE because they cannot accpet.