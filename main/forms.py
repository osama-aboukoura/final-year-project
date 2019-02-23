from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# this class creates the form used in the templates when creating a new user 
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Passwrod must contain at least one digit')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('Passwrod must contain at least one letter')
        if len(password) < 8: 
            raise forms.ValidationError('Passwrod must be at least 8 characters long')
        return password

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
