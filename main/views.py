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
    
    print('user_form')
    print(user_form)
    print('profile_form')
    print(profile_form)
    print('registered')
    print(registered)
    
    return render(request, 'main/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user: 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
            else:
                return HttpResponse("Sorry, Your Account is Not Active")
        else:
            print('log in failed')
            return HttpResponse('Invalid Login Details')
    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def profileInfo(request, user):
    user_ = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=user_)
    print('userProfile ' , userProfile.pk)
    # print('profile ', profile)
    return render(request, 'main/profile.html', {'visited_user':user_, 'visited_userProfile':userProfile})



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


class FlaggedPostsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'main/flagged-posts/flagged-posts.html'
    context_object_name = 'flagged'
    
    def get_queryset(self):
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

        return flagged