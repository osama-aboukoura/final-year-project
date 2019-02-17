from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, UserProfile
from post.models import Post
from comment.models import Comment
from reply.models import Reply
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

        self.reply = Reply.objects.create(
            replytoComment = self.comment,
            replyBy = self.userProfile,
            replyContent = 'That is what I heard.'
        )

        self.client.login(username='osamaaboukoura', password='password123') 

    def test_add_reply_GET_view(self):
        self.set_up()
        response = self.client.get(reverse('reply:add-reply', kwargs={
            'post_pk': self.post.pk, 'comment_pk': self.comment.pk
        }))
        self.assertTemplateUsed(response, 'reply/reply_form.html')
    
    def test_add_reply_POST_view(self):
        self.set_up()
        response = self.client.post(reverse('reply:add-reply', kwargs={
            'post_pk': self.post.pk, 
            'comment_pk': self.comment.pk
        }), {
            'replyBy': self.userProfile,
            'replyContent': 'Good idea.'
        })
        reply = Reply.objects.get(pk=2)
        self.assertEquals(reply.replyContent, 'Good idea.') 
        self.assertEquals(response.status_code, 302) # redirect status code
        
    def test_delete_reply_view(self):
        self.set_up()
        response = self.client.delete(reverse('reply:delete-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }), json.dumps({
            'id': 1
        }))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Reply.objects.count(), 0) # one reply left after deletion 
    
    def test_update_reply_GET_view(self):
        self.set_up()
        response = self.client.get(reverse('reply:edit-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }))
        self.assertTemplateUsed(response, "reply/reply_edit_form.html")
    
    def test_update_reply_POST_view(self):
        self.set_up()
        self.client.post(reverse('reply:edit-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }), {
            'replyContent': 'IT IS VERY EXPENSIVE!'
        })
        self.reply.refresh_from_db()
        self.assertEquals(self.reply.replyContent, 'IT IS VERY EXPENSIVE!') 

    def test_reply_like(self):
        self.set_up()
        # adding a like 
        self.client.get(reverse('reply:like-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }))
        self.assertEquals(self.reply.replyLikes.count(), 1) # reply has 1 like now
        # list of users who liked the reply
        response = self.client.get(reverse('reply:like-list-reply', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, "reply/reply-likes-list.html")
        # removing a like 
        self.client.get(reverse('reply:like-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }))
        self.assertEquals(self.reply.replyLikes.count(), 0) # reply has 0 likes now

    def test_reply_report(self):
        self.set_up()
        self.client.get(reverse('reply:report-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }))
        self.reply.refresh_from_db()
        self.assertEquals(self.reply.replyFlags.count(), 1)

    def test_reply_disable_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('reply:disable-reply', kwargs={'pk': self.reply.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-reply.html") # not used because user isn't staff

    def test_reply_disable_page_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('reply:disable-reply', kwargs={'pk': self.reply.pk}))
        self.assertTemplateUsed(response, "main/flagged-posts/disable-reply.html")
    
    def test_reply_disable_confirm_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('reply:disable-reply-confirm', kwargs={'pk': self.reply.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-reply-confirm.html") 
    
    def test_reply_disable_confirm_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        self.client.get(reverse('reply:disable-reply-confirm', kwargs={'pk': self.reply.pk}))
        self.reply.refresh_from_db()
        self.assertEquals(self.reply.replyDisabled, True)

    def test_reply_remove_flags_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('reply:remove-reply-flags', kwargs={'pk': self.reply.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/remove-flags-reply.html") # not used because user isn't staff

    def test_reply_remove_flags_page_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('reply:remove-reply-flags', kwargs={'pk': self.reply.pk}))
        self.assertTemplateUsed(response, "main/flagged-posts/remove-flags-reply.html")
    
    def test_reply_remove_flags_confirm_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('reply:remove-reply-flags-confirm', kwargs={'pk': self.reply.pk}))
        self.assertTemplateNotUsed(response, "main/flagged-posts/disable-reply-confirm.html") 
    
    def test_reply_remove_flags_confirm_by_staff_member(self):
        self.set_up()
        self.user.is_staff = True
        self.user.save()
        self.client.get(reverse('reply:report-reply', kwargs={
            'post_pk': self.post.pk, 'pk': self.reply.pk
        }))
        self.reply.refresh_from_db()
        self.assertEquals(self.reply.replyFlags.count(), 1)
        self.client.get(reverse('reply:remove-reply-flags-confirm', kwargs={'pk': self.reply.pk}))
        self.reply.refresh_from_db()
        self.assertEquals(self.reply.replyFlags.count(), 0)
