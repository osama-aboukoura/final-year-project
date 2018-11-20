from django.views import generic
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Comment, Reply, UserProfile, User
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and  profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # sets the one to one relationship 

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'post/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user: 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('post:index'))
            else:
                return HttpResponse("Sorry, Your Account is Not Active")
        else:
            print('log in failed')
            return HttpResponse('Invalid Login Details')
    else:
        return render(request, 'post/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post:index'))


class TopicsView(generic.ListView):
    template_name = 'post/topics.html'
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
    template_name = 'post/topic.html'
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
    template_name = 'post/index.html'
    context_object_name = 'all_posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()

class ShowPostView(generic.DetailView):
    model = Post 
    template_name = 'post/post-comment-reply.html'


# def addPostIfLoggedIn(request):
#     user = request.user
#     if user.is_authenticated:
#         return PostCreate.as_view()(request)
#     else:
#         return HttpResponseRedirect(reverse('post:user_login'))

class PostCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post 
    fields = ['postTitle', 'postTopic', 'postContent']

    def form_valid(self, form):
        post = form.save(commit=False)
        logged_in_user = self.request.user
        post.postedBy = logged_in_user
        return super(PostCreate, self).form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post 
    template_name = 'post/post_edit_form.html'
    fields = ['postTitle', 'postTopic', 'postContent']

class PostDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post 
    success_url = reverse_lazy('post:index')


class CommentCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Comment 
    fields = ['commentContent']
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment.commentOnPost = post
        logged_in_user = self.request.user
        comment.commentBy = logged_in_user
        return super(CommentCreate, self).form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        post.postNumberOfComments += 1
        post.save()
        return '/' + str(self.kwargs['pk'])

class CommentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Comment
    template_name = 'post/comment_edit_form.html'
    fields = ['commentContent']

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])

class CommentDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Comment 
    success_url = reverse_lazy('post:index')

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        allreplies = Reply.objects.all()
        post = Post.objects.get(id=self.kwargs['post_pk'])

        for reply in allreplies:
            if reply.replytoComment.pk == comment.pk:
                post.postNumberOfComments -= 1 # decrement 1 for every reply to this comment
        
        post.postNumberOfComments -= 1 # decrement 1 for this comment
        post.save()
        comment.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        return {'post_pk': self.kwargs['post_pk'], 'comment': comment}

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    

class ReplyCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Reply 
    fields = ['replyContent']
    
    def form_valid(self, form):
        reply = form.save(commit=False)
        comment = Comment.objects.get(id=self.kwargs['comment_pk'])
        reply.replytoComment = comment
        logged_in_user = self.request.user
        reply.replyBy = logged_in_user
        return super(ReplyCreate, self).form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments += 1
        post.save()
        return '/' + str(post.pk)

class ReplyUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Reply
    template_name = 'post/reply_edit_form.html'
    fields = ['replyContent']

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    
class ReplyDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Reply 

    def get_context_data(self, **kwargs):
        reply = Reply.objects.get(id=self.kwargs['pk'])
        return {'post_pk': self.kwargs['post_pk'], 'reply': reply}
    
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments -= 1
        post.save()
        return '/' + str(self.kwargs['post_pk'])


def profileInfo(request, user):
    user_ = User.objects.get(username=user)
    userProfile = UserProfile.objects.get(user=user_)
    print('userProfile ' , userProfile.pk)
    # print('profile ', profile)
    return render(request, 'post/profile.html', {'visited_user':user_, 'visited_userProfile':userProfile})


class FlaggedPostsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'post/flagged-posts.html'
    context_object_name = 'flagged'
    
    def get_queryset(self):
        flagged = {'posts':[] , 'comments':[] , 'replies':[]} 

        allposts = Post.objects.all()
        for post in allposts:
            if post.postNumberOfFlags > 0:
                flagged['posts'].append(post)

        allcomments = Comment.objects.all()
        for comment in allcomments:
            if comment.commentNumberOfFlags > 0:
                flagged['comments'].append(comment)
        
        allreplies = Reply.objects.all()
        for reply in allreplies:
            if reply.replyNumberOfFlags > 0:
                flagged['replies'].append(reply)

        return flagged