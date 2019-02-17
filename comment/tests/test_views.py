# from django.test import TestCase, Client
# from django.urls import reverse
# from main.models import User, UserProfile
# from post.models import Post
# from django.contrib.auth import authenticate, login
# import json

# class TestViews(TestCase):

#     def set_up(self):
#         self.client = Client()
#         self.userInstance = User.objects.create(
#             username = 'osamaaboukoura', email = 'osama.aboukoura@kcl.ac.uk'
#         )
#         self.userInstance.set_password('password123')
#         self.userInstance.save() 
        
#         self.userProfileInstance = UserProfile.objects.create (
#             pk = '1', user = self.userInstance,
#         )
#         self.postInstance = Post.objects.create(
#             postedBy = self.userProfileInstance,
#             pk = '1',
#             postTitle = 'Holiday in Istanbul?',
#             postTopic = 'Travel',
#             postContent = 'How much would a 7-nights holiday cost in Istanbul, Turkey?',
#         )
#         self.client.login(username='osamaaboukoura', password='password123') 

#     def test_show_post_with_id_1_GET_view(self):
#         self.set_up()
#         response = self.client.get(reverse('post:show-post', args=['1']))
#         self.assertEquals(response.status_code, 200) # successful request status code
#         self.assertTemplateUsed(response, "post/post-comment-reply.html")
    
#     def test_show_post_with_id_2_GET_view(self):
#         self.set_up()
#         response = self.client.get(reverse('post:show-post', args=['2'])) # post 2 doesn't exist
#         self.assertEquals(response.status_code, 302) # redirect status code
    
#     def test_add_post_GET_view(self):
#         self.set_up()
#         response = self.client.get(reverse('post:add-post'))
#         self.assertTemplateUsed(response, "post/post_form.html")
    
#     def test_add_post_POST_view(self):
#         self.set_up()
#         response = self.client.post(reverse('post:add-post'), {
#             'postedBy': self.userProfileInstance,
#             'postTitle': 'Bitcoin Investment?',
#             'postTopic': 'Finance',
#             'postContent': 'Should I invest in bitcoin, or is it a waste of money?'
#         })
#         post = Post.objects.get(pk=2)
#         self.assertEquals(post.postTitle, 'Bitcoin Investment?') 
#         self.assertEquals(response.status_code, 302) # redirect status code
        
#     def test_delete_post_view(self):
#         response = self.client.delete(reverse('post:delete-post', args=['1']), json.dumps({
#             'id': 1
#         }))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(Post.objects.count(), 0) # zero posts after deletion 
    
#     def test_update_post_GET_view(self):
#         self.set_up()
#         response = self.client.get(reverse('post:edit-post', args=['1']))
#         self.assertTemplateUsed(response, "post/post_edit_form.html")
    
#     def test_update_post_POST_view(self):
#         self.set_up()
#         self.client.post(reverse('post:edit-post', kwargs={'pk': 1}), {
#             'postTitle': 'Holiday in Paris?',
#             'postTopic': 'Holiday', 
#             'postContent': 'How much would a 3-nights holiday cost in Paris, France?'
#         })
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postTitle, 'Holiday in Paris?') 

#     def test_post_like(self):
#         self.set_up()
#         # adding a like 
#         self.client.get(reverse('post:like-post', kwargs={'pk': 1}))
#         self.assertEquals(self.postInstance.postLikes.count(), 1) # post has 1 like now
#         # list of users who liked the post
#         response = self.client.get(reverse('post:like-list-post', kwargs={'pk': 1}))
#         self.assertTemplateUsed(response, "post/post-likes-list.html")
#         # removing a like 
#         self.client.get(reverse('post:like-post', kwargs={'pk': 1}))
#         self.assertEquals(self.postInstance.postLikes.count(), 0) # post has 0 likes now

#     def test_post_vote_up(self):
#         self.set_up()
#         # adding a vote up
#         self.client.get(reverse('post:vote-up-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postVotersUp.count(), 1) # post has 1 vote up now
#         self.assertEquals(self.postInstance.postNumberOfVotes, 1) 
#         # removing a vote up
#         self.client.get(reverse('post:vote-up-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postVotersUp.count(), 0) # post has 1 vote up now
#         self.assertEquals(self.postInstance.postNumberOfVotes, 0) 
    
#     def test_post_vote_down(self):
#         self.set_up()
#         # adding a vote down
#         self.client.get(reverse('post:vote-down-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postVotersDown.count(), 1) # post has 1 vote down now
#         self.assertEquals(self.postInstance.postNumberOfVotes, -1) 
#         # removing a vote down
#         self.client.get(reverse('post:vote-down-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postVotersDown.count(), 0) # post has 0 vote down now
#         self.assertEquals(self.postInstance.postNumberOfVotes, 0) 
        
#     def test_post_report(self):
#         self.set_up()
#         self.client.get(reverse('post:report-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postFlags.count(), 1)

#     def test_post_disable_page_by_regular_user(self):
#         self.set_up()
#         response = self.client.get(reverse('post:disable-post', kwargs={'pk': 1}))
#         self.assertTemplateNotUsed(response, "main/flagged-posts/disable-post.html") # not used because user isn't staff

#     def test_post_disable_page_by_staff_member(self):
#         self.set_up()
#         self.userInstance.is_staff = True
#         self.userInstance.save()
#         response = self.client.get(reverse('post:disable-post', kwargs={'pk': 1}))
#         self.assertTemplateUsed(response, "main/flagged-posts/disable-post.html")
    
#     def test_post_disable_confirm_by_regular_user(self):
#         self.set_up()
#         response = self.client.get(reverse('post:disable-post-confirm', kwargs={'pk': 1}))
#         self.assertTemplateNotUsed(response, "main/flagged-posts/disable-post-confirm.html") 
    
#     def test_post_disable_confirm_by_staff_member(self):
#         self.set_up()
#         self.userInstance.is_staff = True
#         self.userInstance.save()
#         self.client.get(reverse('post:disable-post-confirm', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postDisabled, True)

#     def test_post_remove_flags_page_by_regular_user(self):
#         self.set_up()
#         response = self.client.get(reverse('post:remove-post-flags', kwargs={'pk': 1}))
#         self.assertTemplateNotUsed(response, "main/flagged-posts/remove-flags-post.html") # not used because user isn't staff

#     def test_post_remove_flags_page_by_staff_member(self):
#         self.set_up()
#         self.userInstance.is_staff = True
#         self.userInstance.save()
#         response = self.client.get(reverse('post:remove-post-flags', kwargs={'pk': 1}))
#         self.assertTemplateUsed(response, "main/flagged-posts/remove-flags-post.html")
    
#     def test_post_remove_flags_confirm_by_regular_user(self):
#         self.set_up()
#         response = self.client.get(reverse('post:remove-post-flags-confirm', kwargs={'pk': 1}))
#         self.assertTemplateNotUsed(response, "main/flagged-posts/disable-post-confirm.html") 
    
#     def test_post_remove_flags_confirm_by_staff_member(self):
#         self.set_up()
#         self.userInstance.is_staff = True
#         self.userInstance.save()
#         self.client.get(reverse('post:report-post', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postFlags.count(), 1)
#         self.client.get(reverse('post:remove-post-flags-confirm', kwargs={'pk': 1}))
#         self.postInstance.refresh_from_db()
#         self.assertEquals(self.postInstance.postFlags.count(), 0)
