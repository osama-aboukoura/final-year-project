from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from post.models import Post, UserProfile, User
from comment.models import Comment
from .models import Reply
from django.urls import reverse
from django.urls import reverse_lazy
from post.forms import UserForm, UserProfileForm
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
    template_name = 'reply/reply_edit_form.html'
    fields = ['replyContent']

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    
class ReplyLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            if user in reply.replyLikes.all():
                reply.replyLikes.remove(user)
            else:
                reply.replyLikes.add(user)
        return redirect_url

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

class ReplyReport(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            reply.replyFlags.add(user)
        return redirect_url


class ReplyEnableDisablePage(generic.DeleteView):
    model = Reply
    template_name = 'post/flagged-posts/disable-reply.html'

class ReplyEnableDisable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        reply.replyDisabled = not reply.replyDisabled
        reply.save()
        return redirect_url

class ReplyRemoveFlagsPage(generic.DetailView):
    model = Reply 
    template_name = 'post/flagged-posts/remove-flags-reply.html'

class ReplyRemoveFlags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        reply.replyFlags.clear()
        reply.replyNumberOfFlags = 0
        reply.replyDisabled = False
        reply.save()
        return redirect_url