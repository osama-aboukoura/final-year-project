from django.test import TestCase, Client
from django.urls import reverse, resolve
from post.models import Post
from comment.models import Comment
from reply.models import Reply
from reply.views import *

class TestreplyUrls(TestCase):

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
        self.reply = Reply.objects.create(
            replytoComment = self.comment,
            replyBy = self.userProfile,
            replyContent = 'That is what I heard.'
        )

    def test_add_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:add-reply', kwargs={'post_pk': self.post.pk, 'comment_pk': self.comment.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Create)
    
    def test_edit_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:edit-reply', kwargs={'post_pk': self.post.pk, 'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Update)
    
    def test_delete_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:delete-reply', kwargs={'post_pk': self.post.pk, 'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Delete)
    
    def test_like_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:like-reply', kwargs={'post_pk': self.post.pk, 'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Like)
    
    def test_likes_list_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:like-list-reply', kwargs={'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Likes_List)
    
    def test_report_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:report-reply', kwargs={'post_pk': self.post.pk, 'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Report)
    
    def test_disable_enable_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:disable-reply', kwargs={'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Enable_Disable_Page)
    
    def test_disable_enable_confirm_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:disable-reply-confirm', kwargs={'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Enable_Disable)
    
    def test_remove_flags_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:remove-reply-flags', kwargs={'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Remove_Flags_Page)
    
    def test_remove_flags_confirm_reply_url_resolves(self):
        self.set_up()
        url = reverse('reply:remove-reply-flags-confirm', kwargs={'pk': self.reply.pk})
        self.assertEquals(resolve(url).func.view_class, Reply_Remove_Flags)
