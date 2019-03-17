# To run functional tests you need to have ChromeDriver installed for Chrome version 72
# Then you need to run the command: pip install selenium 
from selenium import webdriver
from django.test import Client
from main.models import User, UserProfile
from post.models import Post
from comment.models import Comment
from reply.models import Reply
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestReply(StaticLiveServerTestCase):
    
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
        self.userProfile = UserProfile.objects.create (user = self.user, numOfPostsCommentsReplies=1)
    
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
    # creates a user, an admin, a post, a comment, a reply and opens up the browser
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
        self.comment= Comment.objects.create(
            commentOnPost = self.post,
            commentBy = self.userProfile,
            commentContent = 'It depends on the hotel you want to stay at, but it will be roughly be around 500 pounds per person.',
        )
        self.reply= Reply.objects.create(
            replytoComment = self.comment,
            replyBy = self.super_userProfile,
            replyContent = 'Thank you!',
        )
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

    # tests the reply adding form by creating a reply on an existing comment
    def test_1_create_reply_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user2', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Reply').click()
        time.sleep(1)
        self.browser.find_element_by_name('replyContent').send_keys(
            'Thanks for the info')
        time.sleep(1)
        self.browser.find_element_by_class_name('submit-button').click()
        time.sleep(2)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h1').text, 
            "Holiday in Istanbul?"
        )
        self.close_down()
        print('Tested create-reply page')

    # tests the reply editing form by editing an existing reply
    def test_2_edit_reply_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user2', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name("reply-ellipsis").click() # this isn't the actual edit button but it still works
        time.sleep(1)
        self.browser.find_element_by_name('replyContent').clear()
        self.browser.find_element_by_name('replyContent').send_keys('Great, Thanks!')
        time.sleep(1)
        self.browser.find_element_by_class_name('submit-button').click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h1').text, 
            "Holiday in Istanbul?"
        )
        self.close_down()
        print('Tested update-reply page')

    # tests the reply like functionality (like and view likes)
    def test_3_like_reply_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name('reply-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('reply-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('reply-like-button').click()
        time.sleep(1)
        self.browser.find_element_by_name('reply-likes').click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_tag_name('h4').text,
            "Users who liked this reply:"
        )
        self.close_down()
        print('Tested reply likes')
    
    # tests the reply report functionality
    def test_4_report_comment_page(self):
        self.set_up()
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_procedure('user1', 'password123')
        time.sleep(1)
        self.browser.find_element_by_link_text("Holiday in Istanbul?").click()
        time.sleep(1)
        self.browser.find_element_by_name('report-reply').click()
        time.sleep(1)
        self.browser.switch_to_alert().accept()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_name('reported-reply').text,
            "- You have reported this reply."
        )
        self.close_down()
        print('Tested reply report')