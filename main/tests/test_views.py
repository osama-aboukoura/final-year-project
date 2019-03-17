from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, UserProfile
from django.contrib import auth

class TestViews(TestCase):

    # set up function that gets called in other functions
    # creates a user and its userProflie 
    def set_up(self):
        self.client = Client()
        self.userInstance = User.objects.create( first_name = 'Osama', username = 'user1', email = 'osama0syrian@gmail.com')
        self.userInstance.set_password('password123')
        self.userInstance.save() 
        self.userProfileInstance = UserProfile.objects.create (
            pk = '1', 
            user = self.userInstance,
            activationCode = '1234'
        )

    # unit test to check a GET request for registering a user 
    def test_user_register_GET_request(self):
        self.set_up()
        response = self.client.get(reverse('main:register'))
        self.assertEquals(response.status_code, 200) # 200 means successful request
        self.assertTemplateUsed(response, "main/authentication/registration.html")

    # unit test to check a POST request for registering a user 
    def test_user_register_POST_request(self):
        self.set_up()
        response = self.client.post(reverse('main:register'), {
            'first_name': 'Osama', 'last_name': 'Aboukoura', 'username': 'osamaaboukoura',
            'email': 'osama.aboukoura@kcl.ac.uk', 'password': 'Password123','profilePicture': None 
        })
        user = User.objects.get(username='osamaaboukoura')
        self.assertEquals(user.email, 'osama.aboukoura@kcl.ac.uk') 
        self.assertEquals(response.status_code, 200) # successful request status code

    # unit test to check a GET request for loggin in a user 
    def test_user_login_GET_request(self):
        self.set_up()
        response = self.client.get(reverse('main:user-login'))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/authentication/login.html")
    
    # unit test to check a GET request for activating in a user 
    def test_user_activate_GET_request(self):
        self.set_up()
        response = self.client.get(reverse('main:activate'))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/authentication/activate.html")

    # unit test to check a POST request for activating in a user 
    def test_user_activate_POST_request(self):
        self.set_up()
        response = self.client.post(reverse('main:activate'), {
            'username': self.userInstance.username,
            'activationCode': self.userProfileInstance.activationCode
        })
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertEquals(self.userInstance.is_active, True) # user is now active 
        self.assertTemplateUsed(response, "main/authentication/login.html")

    # unit test to check a GET request for resending the username
    def test_resend_username_GET_request(self):
        self.set_up()
        response = self.client.get(reverse('main:resend-username'))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/authentication/forgot-username/resend-username.html")

    # unit test to check a POST request for resending the username
    def test_resend_username_POST_request(self):
        self.set_up()
        response = self.client.post(reverse('main:resend-username'), {
            'email': 'osama0syrian@gmail.com' # this won't actually send an email as it is just testing.
        })
        self.assertTemplateUsed(response, "main/authentication/forgot-username/resend_username_email.html")

    # unit test to check a GET request for resetting a password
    def test_reset_password_GET_request(self):
        self.set_up()
        response = self.client.get(reverse('main:reset-password'))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/authentication/forgot-password/reset-password.html")

    # unit test to check a POST request for resetting a password
    def test_reset_password_POST_request(self):
        self.set_up()
        response = self.client.post(reverse('main:reset-password'), {
            'email': 'osama0syrian@gmail.com' # this won't actually send an email as it is just testing.
        })
        self.assertTemplateUsed(response, "main/authentication/forgot-password/reset-password-auth.html")

    # unit test to check a POST request for logging out a user 
    def test_user_logout_POST_request(self):
        self.set_up()
        self.client.login(username='user1', password='password123') 
        self.client.get(reverse('main:user-logout'))
        user = auth.get_user(self.client)
        self.assertNotEquals(str(user), 'user1') # the current user is no longer user1 after logging out
    
    # unit test to check a user's profile page 
    def test_profile_info_view(self):
        self.set_up()
        response = self.client.get(reverse('main:profile', kwargs={
            'user': self.userInstance.username
        }))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/user-profile/profile.html")
    
    # unit test to check a GET request for editing a user's profile 
    def test_edit_profile_info_GET_request(self):
        self.set_up()
        self.client.login(username='user1', password='password123') 
        response = self.client.get(reverse('main:edit-profile', kwargs={
            'user': self.userInstance.username
        }))
        self.assertEquals(response.status_code, 200) # successful request status code
        self.assertTemplateUsed(response, "main/user-profile/profile_edit_form.html")
    
    # unit test to check a POST request for editing a user's profile 
    def test_edit_profile_info_POST_request(self):
        self.set_up()
        self.client.login(username='user1', password='password123') 
        response = self.client.post(reverse('main:edit-profile', kwargs={
            'user': self.userInstance.username
        }), {
            'first_name': 'Osama',
            'last_name': '',
            'profilePicture': None
        })
        self.assertEquals(response.status_code, 200) 
        self.assertEquals(self.userInstance.first_name, 'Osama')
    
    # unit test to check deleting a user's account 
    def test_delete_user_view(self):
        self.set_up()
        response = self.client.get(reverse('main:delete-profile'))
        self.assertTemplateUsed(response, "main/user-profile/delete-user.html")
        
    # unit test to check viewing all topics page 
    def test_view_all_topics(self):
        self.set_up()
        response = self.client.get(reverse('main:topics'))
        self.assertTemplateUsed(response, "main/topics.html")
    
    # unit test to check viewing a single topic page 
    def test_view_specific_topic(self):
        self.set_up()
        response = self.client.get(reverse('main:topic', kwargs={'topic': 'Sports'}))
        self.assertTemplateUsed(response, "main/topic.html")
        
    # unit test to check viewing the main home page 
    def test_view_index(self):
        self.set_up()
        response = self.client.get(reverse('main:index'))
        self.assertTemplateUsed(response, "main/index.html")
        
    # unit test to check viewing the flagged posts page by a basic user 
    def test_flagged_posts_view_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('main:flagged-posts'))
        self.assertTemplateUsed(response, "main/page-not-found.html") # regular users don't have access

    # unit test to check viewing the flagged posts page by a staff member 
    def test_flagged_posts_view_page_by_staff_member(self):
        self.set_up()
        self.userInstance.is_staff = True
        self.userInstance.save()
        self.client.login(username='user1', password='password123') 
        response = self.client.get(reverse('main:flagged-posts'))
        self.assertTemplateUsed(response, "main/flagged-posts/flagged-posts.html")

    # unit test to check viewing the staff page by a basic user
    def test_view_staff_page_by_regular_user(self):
        self.set_up()
        response = self.client.get(reverse('main:staff'))
        self.assertTemplateUsed(response, "main/page-not-found.html") # regular users don't have access

    # unit test to check viewing the staff page by an admin 
    def test_view_staff_page_by_superuser(self):
        self.set_up()
        self.userInstance.is_staff = True
        self.userInstance.is_superuser = True # only admins have access to the staff page
        self.userInstance.save()
        self.client.login(username='user1', password='password123') 
        response = self.client.get(reverse('main:staff'))
        self.assertTemplateUsed(response, "main/staff.html")

    # unit test to check updating staff status by an admin 
    def test_update_staff_status_by_admin(self):
        self.set_up()
        self.userInstance.is_staff = True
        self.userInstance.is_superuser = True # only admins have access to the staff page
        self.userInstance.save()
        self.client.login(username='user1', password='password123') 

        user2 = User.objects.create(username = 'user2', email = 'user2@gmail.com')
        user2.set_password('password123')
        user2.is_staff = True # user2 is a staff member 
        user2.save()
        
        user3 = User.objects.create(username = 'user3', email = 'user3@gmail.com')
        user3.set_password('password123')
        user3.is_staff = False # user3 is a regular member 
        user3.save()

        self.client.get(reverse('main:update-staff', kwargs={'user': user2.username}))
        user2.refresh_from_db()
        self.assertFalse(user2.is_staff) # user2 is now a regular member 

        self.client.get(reverse('main:update-staff', kwargs={'user': user3.username}))
        user3.refresh_from_db()
        self.assertTrue(user3.is_staff) # user3 is now a staff member 

    # unit test to check updating staff status by a basic user 
    def test_update_staff_status_by_regular(self):
        self.set_up()
        self.client.login(username='user1', password='password123') 
        user2 = User.objects.create(username = 'user2', email = 'user2@gmail.com')
        user2.set_password('password123')
        response = self.client.get(reverse('main:update-staff', kwargs={'user': user2.username}))
        self.assertTemplateUsed(response, "main/page-not-found.html") # regular users don't have access

    # unit test to check activating a user by an admin 
    def test_update_active_status_by_admin(self):
        self.set_up()
        self.userInstance.is_staff = True
        self.userInstance.is_superuser = True # only admins have access to the staff page
        self.userInstance.save()
        self.client.login(username='user1', password='password123') 

        user2 = User.objects.create(username = 'user2', email = 'user2@gmail.com')
        user2.set_password('password123')
        user2.is_active = True # user2 is active 
        user2.save()
        
        user3 = User.objects.create(username = 'user3', email = 'user3@gmail.com')
        user3.set_password('password123')
        user3.is_active = False # user3 is not active
        user3.save()

        self.client.get(reverse('main:update-active', kwargs={'user': user2.username}))
        user2.refresh_from_db()
        self.assertFalse(user2.is_active) # user2 is in-active 

        self.client.get(reverse('main:update-active', kwargs={'user': user3.username}))
        user3.refresh_from_db()
        self.assertTrue(user3.is_active) # user3 is now active
