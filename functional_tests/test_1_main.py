# To run functional tests you need to have ChromeDriver installed for Chrome version 72
# Then you need to run the command: pip install selenium 
from selenium import webdriver
from django.test import Client
from main.models import User, UserProfile
from post.models import Post
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestMain(StaticLiveServerTestCase):
    
    # helper functions start here 

    # creates a basic user with its userProfile and stores the records in the database
    def create_regular_user(self):
        self.user = User.objects.create( 
            username = 'user1', 
            email = 'osama.aboukoura@icloud.com',
            first_name = 'Ozzy',
            last_name = 'Aboukoura'
        )
        self.user.set_password('password123')
        self.user.save() 
        self.userProfile = UserProfile.objects.create (user = self.user)
    
    # creates an admin with its userProfile and stores the records in the database
    def create_super_user(self):
        self.super_user = User.objects.create( 
            username = 'user2', 
            email = 'osama.aboukoura@kcl.ac.uk',
            first_name = 'Osama',
            last_name = 'Aboukoura',
            is_staff = True,
            is_superuser = True,
        )
        self.super_user.set_password('password123')
        self.super_user.save() 
        self.super_userProfile = UserProfile.objects.create (user = self.super_user)
    
    # a set up function that gets called in other functions
    # creates a user, an admin, 2 posts and opens up the browser
    def set_up(self):
        self.client = Client()
        self.create_regular_user()
        self.create_super_user()
        self.post= Post.objects.create(
            postedBy = self.userProfile,
            postTitle = 'Holiday in Istanbul?',
            postTopic = 'Travel',
            postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
        )
        self.post.postFlags.add(self.userProfile)
        self.post.save() 
        self.post2 = Post.objects.create(
            postedBy = self.userProfile,
            postTitle = 'Man Utd lost again! Your thoughts?',
            postTopic = 'Sports',
            postContent = 'Manchester United keep losing one game after the other. Why?',
        )
        self.post2.postFlags.add(self.userProfile)
        self.post2.save() 
        self.browser = webdriver.Chrome('functional_tests/chromedriver') # opens up Chrome browser

    # closes the browser at the end of a test
    def close_down(self):
        self.browser.close()

    # takes a username and password for a user and logs them in using the login form
    def login_procedure(self, username, password):
        self.browser.find_element_by_link_text("Login").click()
        time.sleep(1)
        self.browser.find_element_by_name('username').send_keys(username)
        time.sleep(0.5) 
        self.browser.find_element_by_name('password').send_keys(password)
        time.sleep(0.5) 
        self.browser.find_element_by_name('login-button').click()


    # test functions start here 

    # tests the sign up form by creating a user
    def test_1_signup_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.browser.find_element_by_link_text("Sign Up").click()
        time.sleep(1)
        self.browser.find_element_by_name('first_name').send_keys('Bruce')
        time.sleep(0.5)
        self.browser.find_element_by_name('last_name').send_keys('Wayne')
        time.sleep(0.5)
        self.browser.find_element_by_name('username').send_keys('batman')
        time.sleep(0.5) 
        self.browser.find_element_by_name('email').send_keys('osama0syrian@gmail.com')
        time.sleep(0.5) 
        self.browser.find_element_by_name('password').send_keys('password123')
        time.sleep(0.5) 
        self.browser.find_element_by_name('register-button').click()
        time.sleep(2) 
        self.assertEquals(
            self.browser.find_element_by_tag_name('h2').text, 
            "Thank You for Your Registeration!"
        )
        self.close_down()
        print('Tested registeration page')

    # tests the login form by attempting to log a user in
    def test_2_login_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        self.assertEquals(
            self.browser.find_element_by_tag_name('strong').text, 
            self.user.first_name
        )
        self.close_down()
        print('Tested login page')

    # tests functionalities on the profile page (show and edit)
    def test_3_my_profile_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_tag_name('strong').click()
        time.sleep(1)
        self.browser.find_element_by_link_text("My Profile").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Edit Profile").click()
        time.sleep(1)
        self.browser.find_element_by_name('first_name').clear()
        self.browser.find_element_by_name('first_name').send_keys('Osy')
        time.sleep(1)
        self.browser.find_element_by_name('update-button').click()
        time.sleep(1)
        self.assertEquals(self.browser.find_element_by_tag_name('h2').text, "Osy Aboukoura")
        self.close_down()
        print('Tested my-profile page')

    # tests functionalities on the staff page (change staff status and activate/deactivate)
    def test_4_staff_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user2', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Users").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Change to Staff").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Change to Regular User").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Change to Disabled").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Change to Active").click()
        time.sleep(1)
        self.assertEquals(self.browser.find_element_by_tag_name('h1').text, "Admin Panel")
        self.close_down()
        print('Tested staff page')

    # tests functionalities on the flagged posts page (enable/disable delete and remove flags)
    def test_5_flagged_posts_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user2', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Flagged Posts").click()
        time.sleep(1)
        self.browser.find_element_by_name("disable-button").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Disable").click()
        time.sleep(1)
        self.browser.find_element_by_name("enable-button").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Enable").click()
        time.sleep(1)
        self.browser.find_element_by_name("flags-button").click()
        time.sleep(1)
        self.browser.find_element_by_link_text("Remove Flags").click()
        time.sleep(1)
        self.browser.find_element_by_name("delete-button").click()
        time.sleep(1)
        self.browser.find_element_by_name("delete-now").click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h1').text, 
            "All Posts:"
        )
        self.close_down()
        print('Tested flagged-posts page (Enable, Disable, Remove Flags, Delete Post).')