from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)


class UserUpdateForm(forms.ModelForm):
    class Meta():
        model = User 
        fields = ('first_name', 'last_name')


class UserProfileUpdateForm(forms.ModelForm):
    profilePicture = forms.ImageField(required=False)

    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)
