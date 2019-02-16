from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# this class creates the form used in the templates when creating a new user 
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

# this class creates the form used in the templates when creating a profile for a new user 
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)

# this class creates the form used in the templates when editing a user 
class UserUpdateForm(forms.ModelForm):
    class Meta():
        model = User 
        fields = ('first_name', 'last_name')

# this class creates the form used in the templates when editing a profile for a user 
class UserProfileUpdateForm(forms.ModelForm):
    profilePicture = forms.ImageField(required=False)
    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)
