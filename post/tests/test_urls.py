from django.test import SimpleTestCase
from django.urls import reverse, resolve
from post.views import *

class TestPostUrls(SimpleTestCase):

    def test_show_post_url_resolves(self):
        url = reverse('post:show-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Show_Post_View)
    
    def test_add_post_url_resolves(self):
        url = reverse('post:add-post')
        self.assertEquals(resolve(url).func.view_class, Post_Create)
    
    def test_edit_post_url_resolves(self):
        url = reverse('post:edit-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Update)
    
    def test_delete_post_url_resolves(self):
        url = reverse('post:delete-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Delete)
    
    def test_like_post_url_resolves(self):
        url = reverse('post:like-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Like)
    
    def test_likes_list_post_url_resolves(self):
        url = reverse('post:like-list-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Likes_List)
    
    def test_vote_up_post_url_resolves(self):
        url = reverse('post:vote-up-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Vote_Up)
    
    def test_vote_down_post_url_resolves(self):
        url = reverse('post:vote-down-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Vote_Down)
    
    def test_report_post_url_resolves(self):
        url = reverse('post:report-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Report)
    
    def test_disable_enable_post_url_resolves(self):
        url = reverse('post:disable-post', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Enable_Disable_Page)
    
    def test_disable_enable_confirm_post_url_resolves(self):
        url = reverse('post:disable-post-confirm', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Enable_Disable)
    
    def test_remove_flags_post_url_resolves(self):
        url = reverse('post:remove-post-flags', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Remove_Flags_Page)
    
    def test_remove_flags_confirm_post_url_resolves(self):
        url = reverse('post:remove-post-flags-confirm', args=[1])
        self.assertEquals(resolve(url).func.view_class, Post_Remove_Flags)
