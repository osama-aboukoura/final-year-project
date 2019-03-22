from random import randint
from django.views import generic
from django.shortcuts import render
from .models import UserProfile, User
from post.models import Post 
from comment.models import Comment
from reply.models import Reply
from django.urls import reverse
from main.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from .validators import validate_password
import string
import random
from django.core.paginator import Paginator

# registers a new user, sends them an email and saves their profile in the database
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and  profile_form.is_valid():
            user = user_form.save(commit=False) # don't save it in the database yet 

            user.set_password(user.password) # set_password function ensures hashing before saving
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False) # don't save it in the database yet
            profile.user = user # sets the one to one relationship 
            profile.activationCode = randint(1000, 9999)

            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']
                
            registered = True
            profile.save()

            # emailing the user using a html template. if the template doesn't work, a txt file gets used as an alternative 
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
            html = get_template("main/authentication/sign_up_email.html").render({'user': user, 'activationCode': profile.activationCode})
            email.attach_alternative(html, "text/html")
            email.send()

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'main/authentication/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# logs in an existing user 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user: 
            if user.is_active:
                login(request, user)

                # creating a userProfile object for superuser when they log in for the first time. (admins are created through the command line so we have to manually create their userProfile)
                if user.is_superuser:
                    try:
                        userProfile = UserProfile.objects.get(user=user)
                    except UserProfile.DoesNotExist:
                        userProfile = UserProfile.objects.create(user=user)
                        userProfile.save()

                # url to redirect to after logging in
                url_to_redirect_to = request.POST.get('next_url')
                if url_to_redirect_to != 'None/':
                    return HttpResponseRedirect('/' + url_to_redirect_to)

                return HttpResponseRedirect(reverse('main:index'))
            else:
                return HttpResponse("Sorry, Your Account is Not Active") 
        else:
            print('log in failed')
            return render(request, 'main/authentication/login.html', {'error': 'Sorry, unable to log you in.'})
    else:
        url_to_redirect_to = request.GET.get('next')
        return render(request, 'main/authentication/login.html', {'next_url': url_to_redirect_to})

# activates a user that has just signed up
def activate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        activationCode = request.POST.get('activationCode')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None 
        
        if user:
            userProfile = UserProfile.objects.get(user=user)

            if activationCode == userProfile.activationCode: 
                user.is_active = True 
                user.save()
                # changing the activationCode so the user won't be able to activate themselves when Admin disables them.
                userProfile.activationCode = randint(1000, 9999)
                userProfile.save()
                return render(request, 'main/authentication/activate.html', {'activation_success': 'Success! Your account is now activated!'})
            else: 
                return render(request, 'main/authentication/activate.html', {'error': 'Sorry, unable to activate your account.'})

        else:
            return render(request, 'main/authentication/activate.html', {'error': 'Sorry, unable to activate your account.'})
    else:
        return render(request, 'main/authentication/activate.html', {})

# resends the user's username via email 
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

# send the user an email with a passcode to reset their password
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user:
            userProfile = UserProfile.objects.get(user=user)
            # resetPasswordCode is a combination of 15 different letters/numbers 
            userProfile.resetPasswordCode = "".join(random.choices(string.ascii_uppercase + string.digits, k=15))
            userProfile.save() 
            
            # emailing the user with their resetPasswordCode
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

# authenticating the user to reset their password  
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

            if email == userProfile.user.email and temp_code == userProfile.resetPasswordCode: 
                userProfile.resetPasswordCode = "".join(random.choices(string.ascii_uppercase + string.digits, k=15)) # change resetPasswordCode for security reasons
                userProfile.save()
                return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'reset_user_auth': 'Success! You can now reset your password!', 'user': user})
            else: 
                return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {'error': 'Sorry, unable to reset your password'})

        else:
            return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {'error': 'Sorry, unable to reset your password'})
    else:
        return render(request, 'main/authentication/forgot-password/reset-password-auth.html', {})

# resets the user's password 
def reset_password_confirm(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        username = request.POST.get('user')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None 

        if user:
            if password == password_confirm:

                try:
                    validate_password(password) 
                except:
                    return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', 
                    {'error': 'Error, your password should\n - Contain at least 1 letter\n - Contain at least 1 letter\n Be 8 characters long'})

                user.set_password(password)
                user.save()
                return render(request, 'main/authentication/login.html', {'activation_success': 'Success! Your password has been reset!'})
            else: 
                return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'error': 'Sorry, your passwords do not match'})
        else:
            return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {'error': 'Sorry, You cannot reset your password this time.'})
    else:
        return render(request, 'main/authentication/forgot-password/reset-password-confirm.html', {})

# logs out a logged in user
def user_logout(request):
    if (request.user != None):
        logout(request)
    return HttpResponseRedirect(reverse('main:index'))

# displays the user's profile page 
def profile_info(request, user):
    logged_in_user = request.user
    visited_user = User.objects.get(username=user)
    try:
        userProfile = UserProfile.objects.get(user=visited_user)
    except UserProfile.DoesNotExist:
        userProfile = None
    return render(request, 'main/user-profile/profile.html', {'visited_user_profile': userProfile, 'logged_in_user': logged_in_user})

# edits the user's profile page (their name and profile photo)
def edit_profile_info(request, user):
    logged_in_user = request.user    
    user_to_edit = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=user_to_edit)

    if request.method == 'POST':
        user_update_form = UserUpdateForm(data=request.POST)
        profile_update_form = UserProfileUpdateForm(data=request.POST)
        
        if user_update_form.is_valid() and  profile_update_form.is_valid():
            user_to_edit.first_name = request.POST['first_name']
            user_to_edit.last_name = request.POST['last_name']
            user_to_edit.save()

            if 'profilePicture' in request.FILES:
                userProfile.profilePicture = request.FILES['profilePicture']
                userProfile.save() 
            
            return render(request, 'main/user-profile/profile.html', {'visited_user_profile': userProfile, 'logged_in_user': logged_in_user})

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'main/user-profile/profile_edit_form.html', {'user_update_form': user_update_form, 'profile_update_form':profile_update_form})

# takes the user to page asking them to confirm if they want to delete 
def delete_profile_and_user(request):
    logged_in_user = request.user
    return render(request, 'main/user-profile/delete-user.html', {'logged_in_user': logged_in_user})

# deletes the user permanently. removes the posts and likes and everyones' likes, comments and replies on their posts.
def delete_profile_and_user_confirm(request):
    logged_in_user = request.user 
    
    for post in Post.objects.all():
        
        postNumberOfCommentsToDecrement = 0

        if post.postedBy.user == logged_in_user:
            # remove everyone's likes on every post posted by the user we're deleting 
            for userProfile in post.postLikes.all(): 
                userProfile.numberOfLikes -= 1 
                userProfile.save()

            # update the likes & posts count on every comment by all users participating in this post 
            for comment in post.comment_set.all():
                comment.commentBy.numOfPostsCommentsReplies -= 1
                comment.commentBy.save() 

                for userProfile in comment.commentLikes.all(): 
                    userProfile.numberOfLikes -= 1 
                    userProfile.save()

                # update the likes & posts count on every reply by all users replying to this comment 
                for reply in comment.reply_set.all():
                    reply.replyBy.numOfPostsCommentsReplies -= 1
                    reply.replyBy.save() 

                    for userProfile in reply.replyLikes.all(): 
                        userProfile.numberOfLikes -= 1 
                        userProfile.save()

        else:
            for comment in post.comment_set.all():
                if comment.commentBy.user == logged_in_user:
                    postNumberOfCommentsToDecrement += 1  # remove this comment 

                    # remove all users' likes on any comment posted by the user we're deleting 
                    for userProfile in comment.commentLikes.all(): 
                        userProfile.numberOfLikes -= 1 
                        userProfile.save()
                    
                    for reply in comment.reply_set.all():
                        reply.replyBy.numOfPostsCommentsReplies -= 1
                        reply.replyBy.save() 
                        postNumberOfCommentsToDecrement += 1 # remove all replies on this comment 
                else:
                    for reply in comment.reply_set.all():
                        if reply.replyBy.user == logged_in_user:
                            postNumberOfCommentsToDecrement += 1
                            for userProfile in reply.replyLikes.all(): 
                                userProfile.numberOfLikes -= 1 
                                userProfile.save()
                        
        post.postNumberOfComments = post.postNumberOfComments - postNumberOfCommentsToDecrement 
        post.save()

    logout(request)
    logged_in_user.delete() 
    
    return render(request, 'main/index.html', {
        'logged_in_user': logged_in_user, 
        'user_deleted': 'Your account has been deleted!', # a toast message 
        'all_posts': Post.objects.all()
    })

# shows a list of the topics discussed on the site
class Topics_View(generic.ListView):
    template_name = 'main/topics.html'
    context_object_name = 'all_topics'

    def get_queryset(self):
        allposts = Post.objects.all()
        allTopics = {}
        for post in allposts:
            topicWithSpaces = post.postTopic
            topic = post.postTopic.replace(" ", "") # removing the white spaces 
            if topic in allTopics: 
                allTopics[topic][0] += 1 
            else: 
                allTopics[topic] = [1 , topicWithSpaces]
        return allTopics

# shows a list of all the posts that share the same topic 
class Posts_With_Same_Topic_View(generic.ListView):
    template_name = 'main/topic.html'
    context_object_name = 'all_posts'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.kwargs['topic'] # no spaces in between words
        allPostsOfSameTopic = []
        topicToDisplay = '' 
        for post in context['all_posts']:
            if post.postTopic.replace(" ", "") == topic:
                allPostsOfSameTopic.append(post)
                topicToDisplay = post.postTopic

        paginator = Paginator(allPostsOfSameTopic, 8) # 8 posts in one page 
        page = self.request.GET.get('page')
        context['topic'] = topicToDisplay
        context['posts'] = paginator.get_page(page)
        return context

# shows a list of all posts on the site 
class Index_View(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'all_posts'
    model = Post
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['all_posts']:
            post.postTopicNoSpaces = post.postTopic.replace(" ", "")
        return context
    

# shows a list of all flagged posts, comments and replies (after checking if the user is authorised)
def flagged_posts_view(request):
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

# shows a list of all the users on the site (after checking if the user is authorised)
def staff(request):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    users = User.objects.all() 
    return render(request, 'main/staff.html', {'users': users})

# updates the staff status of a user (staff - not staff)
def update_staff_status(request, user):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    user = User.objects.get(username=user)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect('/staff/')

# updates the active status of a user (active - not active)
def update_active_status(request, user):
    logged_in_user = request.user
    if not logged_in_user.is_superuser:
        return render(request, 'main/page-not-found.html')
    user = User.objects.get(username=user)
    user.is_active = not user.is_active
    user.save()
    return HttpResponseRedirect('/staff/')

# displays a page-not-found page (used when anything goes wrong)
def pageNotFound(request):
    return render(request, 'main/page-not-found.html')

# sends an email to staff members when a post/comment/reply is reported
def send_report_email_to_staff(discussion_type, discussion, discussion_by, logged_in_user):
    subject = 'A ' + discussion_type.capitalize() + ' Has Been Reported! - Intelligent Q&A Forums'
    email_to = []
    userProfiles = UserProfile.objects.all()
    for userProfile in userProfiles:
        if userProfile.user.is_staff and userProfile.user != logged_in_user: # don't email yourself if you're staff
            email_to.append(userProfile.user.email)

    with open(settings.BASE_DIR + "/main/templates/main/flagged-posts/report_email.txt") as temp:
        report_email = temp.read()
    email = EmailMultiAlternatives(
        subject=subject, 
        body=report_email,
        from_email=settings.EMAIL_HOST_USER,
        to=email_to
    )
    html = get_template("main/flagged-posts/report_email.html").render({
        'discussion_type': discussion_type, 
        'discussion': discussion, 
        'discussion_by': discussion_by
    })
    email.attach_alternative(html, "text/html")
    email.send()