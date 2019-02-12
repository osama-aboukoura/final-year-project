from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import *

class TestUrls(SimpleTestCase):
    
    def test_register_url_resolves(self):
        url = reverse('main:register')
        self.assertEquals(resolve(url).func, register )
    
    def test_login_url_resolves(self):
        url = reverse('main:user-login')
        self.assertEquals(resolve(url).func, user_login )
    
    def test_logout_url_resolves(self):
        url = reverse('main:user-logout')
        self.assertEquals(resolve(url).func, user_logout )
    
    def test_activate_url_resolves(self):
        url = reverse('main:activate')
        self.assertEquals(resolve(url).func, activate )
    
    def test_resend_username_url_resolves(self):
        url = reverse('main:resend-username')
        self.assertEquals(resolve(url).func, resend_username )
    
    def test_reset_password_url_resolves(self):
        url = reverse('main:reset-password')
        self.assertEquals(resolve(url).func, reset_password )
    
    def test_reset_password_auth_url_resolves(self):
        url = reverse('main:reset-password-auth')
        self.assertEquals(resolve(url).func, reset_password_auth )
    
    def test_reset_password_confirm_url_resolves(self):
        url = reverse('main:reset-password-confirm')
        self.assertEquals(resolve(url).func, reset_password_confirm )

    def test_profile_info_url_resolves(self):
        url = reverse('main:profile', args=['osamaaboukoura'])
        self.assertEquals(resolve(url).func, profile_info )
    
    def test_edit_profile_info_url_resolves(self):
        url = reverse('main:edit-profile', args=['osamaaboukoura'])
        self.assertEquals(resolve(url).func, edit_profile_info )
    
    def test_delete_profile_and_user_url_resolves(self):
        url = reverse('main:delete-profile')
        self.assertEquals(resolve(url).func, delete_profile_and_user )
    
    def test_delete_profile_and_user_confirm_url_resolves(self):
        url = reverse('main:delete-profile-confirm')
        self.assertEquals(resolve(url).func, delete_profile_and_user_confirm )
    
    def test_flagged_posts_url_resolves(self):
        url = reverse('main:flagged-posts')
        self.assertEquals(resolve(url).func, flagged_posts_view )
    
    def test_staff_view_url_resolves(self):
        url = reverse('main:staff')
        self.assertEquals(resolve(url).func, staff )
    
    def test_update_staff_status_url_resolves(self):
        url = reverse('main:update-staff', args=['osamaaboukoura'])
        self.assertEquals(resolve(url).func, update_staff_status )
    
    def test_update_active_status_url_resolves(self):
        url = reverse('main:update-active', args=['osamaaboukoura'])
        self.assertEquals(resolve(url).func, update_active_status )

    def test_index_view_url_resolves(self):
        url = reverse('main:index')
        self.assertEquals(resolve(url).func.view_class, Index_View )
    
    def test_topics_view_url_resolves(self):
        url = reverse('main:topics')
        self.assertEquals(resolve(url).func.view_class, Topics_View )
    
    def test_posts_with_same_topic_url_resolves(self):
        url = reverse('main:topic', args=['sports'])
        self.assertEquals(resolve(url).func.view_class, Posts_With_Same_Topic_View )