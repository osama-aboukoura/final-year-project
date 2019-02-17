# from django.test import TestCase
# from post.models import Post
# from main.models import User, UserProfile

# class TestModels(TestCase):
#     def set_up(self):
#         self.userInstance = User.objects.create(username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk')
#         self.userInstance.set_password('password123')
#         self.userInstance.save() 
#         self.userProfileInstance = UserProfile.objects.create ( pk = '1', user = self.userInstance)
#         self.postInstance = Post.objects.create(
#             postedBy = self.userProfileInstance,
#             postTitle = 'Holiday in Istanbul?',
#             postTopic = 'Travel',
#             postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
#         )
        
#     def test_post_given_a_unique_id_1_on_creation(self):
#         self.set_up()
#         self.assertEquals(self.postInstance.pk, 1) # the first id given is 1 then it auto increments
    
#     def test_post_given_a_unique_id_2_on_creation(self):
#         self.set_up()
#         post = Post.objects.create(
#             postedBy = self.userProfileInstance,
#             postTitle = 'Manchester United haven not lost a game since Jan',
#             postTopic = 'Sports',
#             postContent = 'Ever since Ole Gunner Solkjaer came in as manager, Man Utd are winning their games!',
#         )
#         post.save()
#         self.assertEquals(post.pk, 2) # the first id given is 1 then it auto increments
    
#     def test_post_string_representation(self):
#         self.set_up()
#         self.assertEquals(str(self.postInstance), "Post 1") 