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
    
    def get_context_data(self, **kwargs):
        context = {}
        post = Post.objects.get(id=self.kwargs['pk'])
        context['post'] = post
        logged_in_user = self.request.user
        if logged_in_user.is_authenticated:
            logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
            context['logged_in_user_profile'] = logged_in_user_profile
        
        comments_on_post = post.comment_set.all()
        
        # print(context)

        return context


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
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.num_of_posts_comments_replies = user_profile.num_of_posts_comments_replies + 1
        post.postedBy = user_profile
        user_profile.save()
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
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if user_profile in post.postLikes.all():
                post.postLikes.remove(user_profile)
                user_profile.num_of_likes = post.postedBy.num_of_likes - 1
            else:
                post.postLikes.add(user_profile)
                user_profile.num_of_likes = post.postedBy.num_of_likes + 1
        
        user_profile.save()
        return redirect_url

class PostVoteUp(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)

        if logged_in_user.is_authenticated:
            # if user has already voted down before pressing up, remove the vote down first 
            if logged_in_user_profile in post.postVotersDown.all():
                post.postVotersDown.remove(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes + 1

            if logged_in_user_profile in post.postVotersUp.all():
                post.postVotersUp.remove(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes - 1
            else:
                post.postVotersUp.add(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes + 1
            post.save()
        return redirect_url

class PostVoteDown(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)

        if logged_in_user.is_authenticated:
             # if user has already voted up before pressing down, remove the vote up first 
            if logged_in_user_profile in post.postVotersUp.all():
                post.postVotersUp.remove(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes - 1

            if logged_in_user_profile in post.postVotersDown.all():
                post.postVotersDown.remove(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes + 1
                post.save()
            else:
                post.postVotersDown.add(logged_in_user_profile)
                post.postNumberOfVotes = post.postNumberOfVotes - 1
                post.save()
        return redirect_url

class PostDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post 

    def get_success_url(self):
        return reverse_lazy('main:index')

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        author_profile = post.postedBy
        # user_profile = get_object_or_404(UserProfile, user=post_owner)
        author_profile.num_of_posts_comments_replies = author_profile.num_of_posts_comments_replies - 1

        # removing the like on the post 
        if author_profile in post.postLikes.all():
            author_profile.num_of_likes = author_profile.num_of_likes - 1

        # removing comments and any likes on all the comments on this post 
        comments_on_post = post.comment_set.all()
        for comment in comments_on_post:
            if author_profile == comment.commentBy:
                author_profile.num_of_posts_comments_replies = author_profile.num_of_posts_comments_replies - 1
            if author_profile in comment.commentLikes.all():
                author_profile.num_of_likes = author_profile.num_of_likes - 1
                # WHAT ABOUT THE COMMENTS FOR OTHER USERS? TO FIX LATER

        author_profile.save()
        post.delete()
        return HttpResponseRedirect(self.get_success_url())
        
class PostReport(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            post.postFlags.add(logged_in_user_profile)
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

