from django.test import TestCase
from main.models import User, UserProfile

class TestModels(TestCase):
    def set_up(self):
        self.user = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
        self.user.set_password('password123')
        self.user.save() 
        self.userProfile = UserProfile.objects.create (user = self.user)
        
    def test_user_given_a_unique_primay_key(self):
        self.set_up()
        # user has a unique primary key in addition to the unique username 
        self.assertEquals(self.user.pk, 1) 

    def test_userProfile_given_a_unique_primay_key(self):
        self.set_up()
        # userProfile has a unique primary key in addition to the unique username 
        self.assertEquals(self.userProfile.pk, 1) 
        
    def test_user_string_representation_is_equal_to_username(self):
        self.set_up()
        self.assertEquals(str(self.user), "osamaaboukoura") 
    
    def test_userProfile_string_representation_is_equal_to_username(self):
        self.set_up()
        self.assertEquals(str(self.userProfile), "osamaaboukoura") 