from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label=('First Name'))
    last_name = forms.CharField(required=True, label=('Last Name'))

    class Meta():
        model = UserProfile 
        fields = ('first_name', 'last_name', 'profile_picture',)
