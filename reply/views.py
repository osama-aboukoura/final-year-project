from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from post.models import Post
from comment.models import Comment
from .models import Reply
from django.urls import reverse
from django.urls import reverse_lazy
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class ReplyCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Reply 
    fields = ['replyContent']
    
    def form_valid(self, form):
        reply = form.save(commit=False)
        comment = Comment.objects.get(id=self.kwargs['comment_pk'])
        reply.replytoComment = comment
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.num_of_posts_comments_replies = user_profile.num_of_posts_comments_replies + 1
        reply.replyBy = user_profile
        user_profile.save()
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
    template_name = 'reply/reply_edit_form.html'
    fields = ['replyContent']

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    
class ReplyLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if logged_in_user_profile in reply.replyLikes.all():
                reply.replyLikes.remove(logged_in_user_profile)
                logged_in_user_profile.num_of_likes = logged_in_user_profile.num_of_likes - 1
            else:
                reply.replyLikes.add(logged_in_user_profile)
                logged_in_user_profile.num_of_likes = logged_in_user_profile.num_of_likes + 1
        logged_in_user_profile.save()
        return redirect_url

class ReplyDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Reply 

    def delete(self, request, *args, **kwargs):
        # post = Post.objects.get(id=self.kwargs['post_pk']) # STILL NEED TO DECREESE THE TOTAL NUMBER OF COMMENTS(REPLIES) AFTER DELETING
        
        reply = self.get_object()
        author_profile = reply.replyBy
        author_profile.num_of_posts_comments_replies = author_profile.num_of_posts_comments_replies - 1
        
        # removing the like on the reply 
        if author_profile in reply.replyLikes.all():
            author_profile.num_of_likes = author_profile.num_of_likes - 1

        author_profile.save()
        reply.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments -= 1
        post.save()
        return '/' + str(self.kwargs['post_pk'])

class ReplyReport(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            reply.replyFlags.add(logged_in_user_profile)
        return redirect_url


class ReplyEnableDisablePage(generic.DeleteView):
    model = Reply
    template_name = 'main/flagged-posts/disable-reply.html'

class ReplyEnableDisable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        reply.replyDisabled = not reply.replyDisabled
        reply.save()
        return redirect_url

class ReplyRemoveFlagsPage(generic.DetailView):
    model = Reply 
    template_name = 'main/flagged-posts/remove-flags-reply.html'

class ReplyRemoveFlags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        reply.replyFlags.clear()
        reply.replyNumberOfFlags = 0
        reply.replyDisabled = False
        reply.save()
        return redirect_url