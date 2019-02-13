from django.test import TestCase, Client
from django.urls import reverse
from main.models import User, UserProfile
import json

# class TestViews(TestCase):

#     def set_up(self):
#         self.client = Client()
