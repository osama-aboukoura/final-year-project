from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from .models import UserProfile, User
from post.models import Post 
from comment.models import Comment
from reply.models import Reply
from django.urls import reverse
from django.urls import reverse_lazy
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound

def register(request):
    registered = False
    if request.method == 'POST':
        print ('post request')
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and  profile_form.is_valid():
            print('form valid and profile form valid')
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # sets the one to one relationship 

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                
            registered = True
            profile.save()

        else:
            print('erros in form')
            print(user_form.errors,profile_form.errors)
    else:
        print ('get request')
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'main/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        print('user')
        print(user)

        if user: 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
            else:
                # DOESN'T WORK FOR SOME REASON!!!!!
                return HttpResponse("Sorry, Your Account is Not Active") 
        else:
            print('log in failed')
            return render(request, 'main/login.html', {'error': 'Sorry, unable to log you in.'})
    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def profileInfo(request, user):
    visited_user = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=visited_user)
    return render(request, 'main/profile.html', {'visited_user_profile': userProfile})



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