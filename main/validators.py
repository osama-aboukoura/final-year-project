from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_name(name):
    if len(name) < 2: 
        raise ValidationError('This name field must be at least 2 characters long.')
    return name

def validate_email(email):
    all_users = User.objects.all()
    for user in all_users:
        if user.email == email: 
            raise ValidationError('A user with that email address already exists.')
    return email

def validate_password(password):
    if not any(char.isdigit() for char in password):
        raise ValidationError('Passwrod must contain at least one digit.')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Passwrod must contain at least one letter.')
    if len(password) < 8: 
        raise ValidationError('Passwrod must be at least 8 characters long.')
    return password