from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from .models import Post
from comment.models import Comment
from reply.models import Reply
from django.urls import reverse
from django.urls import reverse_lazy
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


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

class PostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            if user in post.postLikes.all():
                post.postLikes.remove(user)
            else:
                post.postLikes.add(user)
        return redirect_url

class PostVoteUp(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        # if user has already voted down before pressing up, remove the vote down first 
        if user.is_authenticated:
            if user in post.postVotersDown.all():
                post.postVotersDown.remove(user)
                post.postNumberOfVotes = post.postNumberOfVotes + 1

            if user in post.postVotersUp.all():
                post.postVotersUp.remove(user)
                post.postNumberOfVotes = post.postNumberOfVotes - 1
                post.save()
            else:
                post.postVotersUp.add(user)
                post.postNumberOfVotes = post.postNumberOfVotes + 1
                post.save()
        return redirect_url

class PostVoteDown(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user
        # if user has already voted up before pressing down, remove the vote up first 
        if user in post.postVotersUp.all():
                post.postVotersUp.remove(user)
                post.postNumberOfVotes = post.postNumberOfVotes - 1

        if user.is_authenticated:
            if user in post.postVotersDown.all():
                post.postVotersDown.remove(user)
                post.postNumberOfVotes = post.postNumberOfVotes + 1
                post.save()
            else:
                post.postVotersDown.add(user)
                post.postNumberOfVotes = post.postNumberOfVotes - 1
                post.save()
        return redirect_url

class PostDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post 
    success_url = reverse_lazy('post:index')

class PostReport(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            post.postFlags.add(user)
        return redirect_url

class PostEnableDisablePage(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/disable-post.html'

class PostEnableDisable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        post.postDisabled = not post.postDisabled
        post.save()
        return redirect_url

class PostRemoveFlagsPage(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/remove-flags-post.html'

class PostRemoveFlags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        post.postFlags.clear()
        post.postNumberOfFlags = 0
        post.postDisabled = False
        post.save()
        return redirect_url

