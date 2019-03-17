from django.test import TestCase
from main.models import User, UserProfile

class TestModels(TestCase):

    # set up function that gets called in other functions
    # creates a user and its userProflie 
    def set_up(self):
        self.user = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
        self.user.set_password('password123')
        self.user.save() 
        self.userProfile = UserProfile.objects.create (user = self.user)
    
    # unit test to check the uniqueness of the primary key of a user 
    def test_user_given_a_unique_primay_key(self):
        self.set_up()
        self.assertEquals(self.user.pk, 1) 

    # unit test to check the uniqueness of the primary key of a userProfile
    def test_userProfile_given_a_unique_primay_key(self):
        self.set_up()
        self.assertEquals(self.userProfile.pk, 1) 
        
    # unit test to check the string representation of a user 
    def test_user_string_representation_is_equal_to_username(self):
        self.set_up()
        self.assertEquals(str(self.user), "osamaaboukoura") 

    # unit test to check the string representation of a userProfile
    def test_userProfile_string_representation_is_equal_to_username(self):
        self.set_up()
        self.assertEquals(str(self.userProfile), "osamaaboukoura") 