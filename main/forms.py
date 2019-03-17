from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .validators import validate_email, validate_name, validate_password

# creates the form used in the templates when creating a new user 
class UserForm(forms.ModelForm):

    # overiding the __init__ function to remove the form's help_text
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None # help text: "Required. 150 characters or fewer...etc"

    # adding validators to the form fields 
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    first_name = forms.CharField(validators=[validate_name])
    last_name = forms.CharField(validators=[validate_name])

    class Meta():
        model = User 
        # fields to display to the user
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

# creates the form used in the templates when creating a profile for a new user 
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)

# creates the form used in the templates when editing a user 
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(validators=[validate_name])
    last_name = forms.CharField(validators=[validate_name])

    class Meta():
        model = User 
        # fields to display to the user
        fields = ('first_name', 'last_name',)

# creates the form used in the templates when editing a profile for a user 
class UserProfileUpdateForm(forms.ModelForm):
    profilePicture = forms.ImageField(required=False)
    class Meta():
        model = UserProfile 
        fields = ('profilePicture',)
