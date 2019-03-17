# To run functional tests you need to have ChromeDriver installed for Chrome version 72
# Then you need to run the command: pip install selenium 
from selenium import webdriver
from django.test import Client
from main.models import User, UserProfile
from post.models import Post
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestPost(StaticLiveServerTestCase):
    
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
        self.super_userProfile = UserProfile.objects.create (user = self.super_user, numOfPostsCommentsReplies=1)
    
    # a set up function that gets called in other functions
    # creates a user, an admin, a post and opens up the browser
    def set_up(self):
        self.client = Client()
        self.create_regular_user()
        self.create_super_user()
        self.post= Post.objects.create(
            postedBy = self.super_userProfile,
            postTitle = 'Holiday in Istanbul?',
            postTopic = 'Travel',
            postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
        )
        self.post.save() 
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

    # tests the post adding form by creating a post
    def test_1_create_post_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Add New Post").click()
        time.sleep(1)
        self.browser.find_element_by_name('postTitle').send_keys('What course do I study at university?')
        time.sleep(1)
        self.browser.find_element_by_name('postTopic').send_keys('Education')
        time.sleep(1)
        self.browser.find_element_by_name('postContent').send_keys(
            'I have recently finished my A-levels and I\'m wondering what course to do at university. Any recommendations?')
        time.sleep(1)
        self.browser.find_element_by_class_name('submit-button').click()
        time.sleep(2)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h1').text, 
            "What course do I study at university?"
        )
        self.close_down()
        print('Tested create-post page')

    # tests the post editing form by editing an existing post
    def test_2_edit_post_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user2', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name("post-ellipsis").click() # this isn't the actual edit button but it still works
        time.sleep(1)
        self.browser.find_element_by_name('postTitle').clear()
        self.browser.find_element_by_name('postTitle').send_keys('Holiday in Paris?')
        time.sleep(1)
        self.browser.find_element_by_name('postContent').clear()
        self.browser.find_element_by_name('postContent').send_keys(
            'How much would a 5-nights holiday cost in Paris, France?')
        time.sleep(1)
        self.browser.find_element_by_class_name('submit-button').click()
        time.sleep(2)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h1').text, 
            "Holiday in Paris?"
        )
        self.close_down()
        print('Tested update-post page')

    # tests the post like functionality (like and view likes)
    def test_3_like_post_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name('post-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('post-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('post-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('post-likes').click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h4').text,
            "Users who liked this post:"
        )
        self.close_down()
        print('Tested post likes')

    # tests the post voting functionality (vote up/down)
    def test_4_vote_up_and_down_post(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name('vote-up-post').click()
        time.sleep(1)
        self.browser.find_element_by_name('vote-up-post').click()
        time.sleep(1)
        self.browser.find_element_by_name('vote-down-post').click()
        time.sleep(1)
        self.browser.find_element_by_name('vote-down-post').click()
        time.sleep(1)
        self.browser.find_element_by_name('vote-down-post').click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_name('postNumberOfVotes').text,
            "-1"
        )
        self.close_down()
        print('Tested post votes')

    # tests the post report functionality
    def test_5_report_post_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name('report-post').click()
        time.sleep(1)
        self.browser.switch_to_alert().accept()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_name('reported-post').text,
            "- You have reported this post."
        )
        self.close_down()
        print('Tested post report')
