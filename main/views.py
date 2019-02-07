from random import randint
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from .models import UserProfile, User
from post.models import Post 
from comment.models import Comment
from reply.models import Reply
from django.urls import reverse
from django.urls import reverse_lazy
from main.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.template import RequestContext
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
import string
import random

def register(request):
    registered = False
    if request.method == 'POST':
        print ('post request')
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and  profile_form.is_valid():
            print('form valid and profile form valid')
            user = user_form.save(commit=False)

            all_users = User.objects.all()
            for _user in all_users:
                if _user.email == user.email: 
                    return render(request, 'main/authentication/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error': 'Email address already used.'})

            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # sets the one to one relationship 
            profile.activation_code = randint(1000, 9999)

            if 'profile_picture' in request.FILES:
                print ('profile_picture is in request.FILES')
                profile.profile_picture = request.FILES['profile_picture']
                
            registered = True
            profile.save()

            subject = 'Welcome! - Intelligent Q&A Forums'
            email_to = [user.email] 
            with open(settings.BASE_DIR + "/main/templates/main/authentication/sign_up_email.txt") as temp:
                sign_up_email = temp.read()
            email = EmailMultiAlternatives(
                subject=subject, 
                body=sign_up_email,
                from_email=settings.EMAIL_HOST_USER,
                to=email_to
            )
            html = get_template("main/authentication/sign_up_email.html").render({'user': user, 'activation_code': profile.activation_code})
            email.attach_alternative(html, "text/html")
            email.send()

        else:
            print('erros in form')
            print(user_form.errors,profile_form.errors)
    else:
        print ('get request')
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'main/authentication/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user: 
            if user.is_active:
                login(request, user)
                # redirect_to = request.get('next', '')
                # if redirect_to:
                #     print ('redirect_to')
                #     print (redirect_to)
                return HttpResponseRedirect(reverse('main:index'))
            else:
                # DOESN'T WORK FOR SOME REASON!!!!!
                return HttpResponse("Sorry, Your Account is Not Active") 
        else:
            print('log in failed')
            return render(request, 'main/authentication/login.html', {'error': 'Sorry, unable to log you in.'})
    else:
        return render(request, 'main/authentication/login.html', {})


def activate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        activation_code = request.POST.get('activation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None 
        
        if user:
            userProfile = UserProfile.objects.get(user=user)

            if activation_code == userProfile.activation_code: 
                user.is_active = True 
                user.save()
                # changing the activation_code so the user won't be able to activate themselves when Admin disables them.
                userProfile.activation_code = randint(1000, 9999)
                userProfile.save()
                return render(request, 'main/authentication/login.html', {'activation_success': 'Success! Your account is now activated!'})
            else: 
                return render(request, 'main/authentication/activate.html', {'error': 'Sorry, unable to activate your account.'})

        else:
            return render(request, 'main/authentication/activate.html', {'error': 'Sorry, unable to activate your account.'})
    else:
        return render(request, 'main/authentication/activate.html', {})


def resend_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user:
            subject = 'Your Username - Intelligent Q&A Forums'
            email_to = [user.email] 
            with open(settings.BASE_DIR + "/main/templates/main/authentication/forgot-username/resend_username_email.txt") as temp:
                resend_username_email = temp.read()
            email = EmailMultiAlternatives(
                subject=subject, 
                body=resend_username_email,
                from_email=settings.EMAIL_HOST_USER,
                to=email_to
            )
            html = get_template("main/authentication/forgot-username/resend_username_email.html").render({'user': user})
            email.attach_alternative(html, "text/html")
            email.send()
        
        return render(request, 'main/authentication/login.html', {'activation_success': 'If your email address is linked with an account, an email will be sent to you with your username.'})

    else:
        return render(request, 'main/authentication/forgot-username/resend-username.html', {})


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user:
            userProfile = UserProfile.objects.get(user=user)

            userProfile.reset_password_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=15))
            userProfile.save() 
            print ('userProfile.reset_password_code')
            print (userProfile.reset_password_code)

            subject = 'Reset your Password - Intelligent Q&A Forums'
            email_to = [userProfile.user.email] 
            with open(settings.BASE_DIR + "/main/templates/main/authentication/forgot-password/reset_password_email.txt") as temp:
                reset_password_email = temp.read()
            email = EmailMultiAlternatives(
                subject=subject, 
                body=reset_password_email,
                from_email=settings.EMAIL_HOST_USER,
                to=email_to
            )
            html = get_template("main/authentication/forgot-password/reset_password_email.html").render({'userProfile': userProfile})
            email.attach_alternative(html, "text/html")
            email.send()

        return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {'reset_password_email_sent': 'If the email address is correct, a temp code will be sent to you.'})

    else:
        return render(request, 'main/authentication/forgot-password/reset-password.html', {})

def reset_password_auth(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        temp_code = request.POST.get('temp_code')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None 
        
        if user:
            userProfile = UserProfile.objects.get(user=user)

            if email == userProfile.user.email and temp_code == userProfile.reset_password_code: 
                return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'reset_user_auth': 'Success! You can now reset your password!', 'user': user})
            else: 
                return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {'error': 'Sorry, unable to reset your password'})

        else:
            return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {'error': 'Sorry, unable to reset your password'})
    else:
        return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {})


def reset_password_confirm(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        username = request.POST.get('user')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None 

        print ('user to update passworddd')
        print (user)

        if user:
            if password == password_confirm:
                user.set_password(password)
                try:
                    # change the current reset_password_code so that it cannot be used twice 
                    userProfile = UserProfile.objects.get(user=user)
                    userProfile.reset_password_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=15))
                    userProfile.save() 
                except UserProfile.DoesNotExist:
                    userProfile = None 
                user.save()
                return render(request, 'main/authentication/login.html', {'activation_success': 'Success! Your password has been reset!'})
            else: 
                return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'error': 'Sorry, your passwords do not match'})
        else:
            return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'error': 'Sorry, You cannot reset your password this time.'})
    else:
        return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {})

    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def profileInfo(request, user):
    logged_in_user = request.user
    visited_user = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=visited_user)
    return render(request, 'main/user-profile/profile.html', {'visited_user_profile': userProfile, 'logged_in_user': logged_in_user})

def editprofileInfo(request, user):
    logged_in_user = request.user    
    user_to_edit = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=user_to_edit)

    if request.method == 'POST':
        user_to_edit.first_name = request.POST['first_name']
        user_to_edit.last_name = request.POST['last_name']
        user_to_edit.save()

        if 'profile_picture' in request.FILES:
            userProfile.profile_picture = request.FILES['profile_picture']
            userProfile.save() 
        
        return render(request, 'main/user-profile/profile.html', {'visited_user_profile': userProfile, 'logged_in_user': logged_in_user})

    else:
        print('GET REQUEST ')
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = UserProfileUpdateForm(instance=request.user)
        # return render(request, 'main/profile_edit_form.html', {'form': form})
        return render(request, 'main/user-profile/profile_edit_form.html', {'user_update_form': user_update_form, 'profile_update_form':profile_update_form})


def deleteProfileAndUser(request):
    logged_in_user = request.user
    return render(request, 'main/user-profile/delete-user.html', {'logged_in_user': logged_in_user})

def deleteProfileAndUserConfirm(request):
    logged_in_user = request.user 
    
    for post in Post.objects.all():
        
        postNumberOfCommentsToDecrement = 0

        if post.postedBy.user == logged_in_user:
            print ('1 post owner about to be deleted')
            # remove everyone's likes on every post posted by the user we're deleting 
            for userProfile in post.postLikes.all(): 
                userProfile.num_of_likes -= 1 
                userProfile.save()
                print ('4 updating profile num_of_likes')

            # update the likes & posts count on every comment by all users participating in this post 
            for comment in post.comment_set.all():
                comment.commentBy.num_of_posts_comments_replies -= 1
                comment.commentBy.save() 
                print ('5 updating profile num_of_posts_comments_replies')

                for userProfile in comment.commentLikes.all(): 
                    userProfile.num_of_likes -= 1 
                    userProfile.save()
                    print ('6 updating profile num_of_likes')

                # update the likes & posts count on every reply by all users replying to this comment 
                for reply in comment.reply_set.all():
                    reply.replyBy.num_of_posts_comments_replies -= 1
                    reply.replyBy.save() 
                    print ('7 updating profile num_of_posts_comments_replies')

                    for userProfile in reply.replyLikes.all(): 
                        userProfile.num_of_likes -= 1 
                        userProfile.save()
                        print ('8 updating profile num_of_likes')

        else:
            print ('2 user to delete is not post owner')
            for comment in post.comment_set.all():
                if comment.commentBy.user == logged_in_user:
                    postNumberOfCommentsToDecrement += 1  # remove this comment 

                    # remove all users' likes on any comment posted by the user we're deleting 
                    for userProfile in comment.commentLikes.all(): 
                        userProfile.num_of_likes -= 1 
                        userProfile.save()
                    
                    for reply in comment.reply_set.all():
                        reply.replyBy.num_of_posts_comments_replies -= 1
                        reply.replyBy.save() 
                        postNumberOfCommentsToDecrement += 1 # remove all replies on this comment 
                else:
                    print ('3 user is not comment owner')
                    for reply in comment.reply_set.all():
                        if reply.replyBy.user == logged_in_user:
                            postNumberOfCommentsToDecrement += 1
                            for userProfile in reply.replyLikes.all(): 
                                userProfile.num_of_likes -= 1 
                                userProfile.save()
                        
        post.postNumberOfComments = post.postNumberOfComments - postNumberOfCommentsToDecrement 
        post.save()

    logout(request)
    logged_in_user.delete() 
    
    return render(request, 'main/index.html', {
        'logged_in_user': logged_in_user, 
        'user_deleted': 'Your account has been deleted!',
        'all_posts': Post.objects.all()
    })
    # return reverse_lazy('main:index' , kwargs={)
    # return HttpResponseRedirect(reverse('main:index'), kwargs={})

    # user_to_edit = User.objects.get(username=user)
    # userProfile = UserProfile.objects.get(user=user_to_edit)
    # return render(request, 'main/profile.html', {'visited_user_profile': userProfile})

# class ProfileUpdate(LoginRequiredMixin, UpdateView):
#     login_url = '/login/'
#     model = UserProfile 
#     template_name = 'main/profile_edit_form.html'
#     fields = ['user', 'first_name']  

#     def get_success_url(self):
#         profile = get_object_or_404(UserProfile, id= self.kwargs.get('pk'))
#         user = profile.user
#         return reverse_lazy('main:profile' , kwargs={'user': user})

class TopicsView(generic.ListView):
    template_name = 'main/topics.html'
    context_object_name = 'all_topics'

    def get_queryset(self):
        allposts = Post.objects.all()
        allTopics = {}
        for post in allposts:
            topic = post.postTopic
            if topic in allTopics: 
                allTopics[topic] += 1 
            else: 
                allTopics[topic] = 1 
        return allTopics

class PostsWithSameTopicView(generic.ListView):
    template_name = 'main/topic.html'
    context_object_name = 'all_posts'
    
    def get_queryset(self):
        topic = self.kwargs['topic']
        allPosts = Post.objects.all()
        allPostsOfSameTopic = []
        for post in allPosts:
            if post.postTopic == topic:
                allPostsOfSameTopic.append(post)
        return { 'topic': topic, 'posts': allPostsOfSameTopic }

class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'all_posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()



def flaggedPostsView(request):
    logged_in_user = request.user
    if not logged_in_user.is_staff:
        return render(request, 'main/page-not-found.html')

    flagged = {'posts':[] , 'comments':[] , 'replies':[]} 

    allposts = Post.objects.all()
    for post in allposts:
        if post.postFlags.count() > 0:
            flagged['posts'].append(post)

    allcomments = Comment.objects.all()
    for comment in allcomments:
        if comment.commentFlags.count() > 0:
            flagged['comments'].append(comment)
    
    allreplies = Reply.objects.all()
    for reply in allreplies:
        if reply.replyFlags.count() > 0:
            flagged['replies'].append(reply)

    return render(request, 'main/flagged-posts/flagged-posts.html', {'flagged': flagged})

def staff(request):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    users = User.objects.all() 
    return render(request, 'main/staff.html', {'users': users})

def updateStaffStatus(request, user):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    user = User.objects.get(username=user)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect('/staff/')

def updateActiveStatus(request, user):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    user = User.objects.get(username=user)
    user.is_active = not user.is_active
    user.save()
    return HttpResponseRedirect('/staff/')

def pageNotFound(request):
    return render(request, 'main/page-not-found.html')
