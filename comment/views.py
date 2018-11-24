from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from post.models import Post, UserProfile, User
from reply.models import Reply
from .models import Comment
from django.urls import reverse
from django.urls import reverse_lazy
from post.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = 'comment/comment_edit_form.html'
    fields = ['commentContent']

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])

class CommentLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            if user in comment.commentLikes.all():
                comment.commentLikes.remove(user)
            else:
                comment.commentLikes.add(user)
        return redirect_url

class CommentVoteUp(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        # if user has already voted down before pressing up, remove the vote down first 
        if user in comment.commentVotersDown.all():
                comment.commentVotersDown.remove(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1

        if user.is_authenticated:
            if user in comment.commentVotersUp.all():
                comment.commentVotersUp.remove(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1
                comment.save()
            else:
                comment.commentVotersUp.add(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1
                comment.save()
        return redirect_url

class CommentVoteDown(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        # if user has already voted up before pressing down, remove the vote up first 
        if user in comment.commentVotersUp.all():
                comment.commentVotersUp.remove(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1

        if user.is_authenticated:
            if user in comment.commentVotersDown.all():
                comment.commentVotersDown.remove(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1
                comment.save()
            else:
                comment.commentVotersDown.add(user)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1
                comment.save()
        return redirect_url

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
    
class CommentReport(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        user = self.request.user 
        if user.is_authenticated:
            comment.commentFlags.add(user)
        return redirect_url


class CommentEnableDisablePage(generic.DeleteView):
    model = Comment
    template_name = 'post/flagged-posts/disable-comment.html'

class CommentEnableDisable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        comment.commentDisabled = not comment.commentDisabled
        comment.save()
        return redirect_url

class CommentRemoveFlagsPage(generic.DetailView):
    model = Comment 
    template_name = 'post/flagged-posts/remove-flags-comment.html'

class CommentRemoveFlags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        comment.commentFlags.clear()
        comment.commentNumberOfFlags = 0
        comment.commentDisabled = False
        comment.save()
        return redirect_url
