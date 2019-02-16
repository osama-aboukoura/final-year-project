from django.test import TestCase
from main.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm

class TestForms(TestCase):
    def test_user_create_form_valid(self):
        form = UserForm(data={
            'first_name': 'Osama',
            'last_name': 'Aboukoura',
            'username': 'osamaaboukoura',
            'email': 'osama.aboukoura@kcl.ac.uk',
            'password': 'Password123'
        })
        self.assertTrue(form.is_valid())

    def test_user_create_form_invalid(self):
        form = UserForm(data={
            'first_name': 'Osama',
            'last_name': '', # this shouldn't cause an error. not a compulsory field.
            'username': 'osamaaboukoura',
            'email': 'osama.aboukoura@', # this should cause an error: invalid email.
            'password': 'Password123'
        })
        self.assertFalse(form.is_valid()) # an invalid form 
        self.assertEquals(len(form.errors), 1) # total number of errors in the form.

    def test_userProfile_create_form_valid(self):
        form = UserProfileForm(data={
            'profilePicture': None # a display photo is not compulsory 
        })
        self.assertTrue(form.is_valid())

    def test_user_update_form_valid(self):
        form = UserUpdateForm(data={
            'first_name': 'Osy',
            'last_name': 'ab'
        })
        self.assertTrue(form.is_valid())

    def test_userProfile_update_form_valid(self):
        form = UserProfileUpdateForm(data={
            'profilePicture': None
        })
        self.assertTrue(form.is_valid())