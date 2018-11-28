from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from post.models import Post
from reply.models import Reply
from .models import Comment
from django.urls import reverse
from django.urls import reverse_lazy
from main.forms import UserForm, UserProfileForm
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
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.num_of_posts_comments_replies = user_profile.num_of_posts_comments_replies + 1
        comment.commentBy = user_profile
        user_profile.save()
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
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if logged_in_user_profile in comment.commentLikes.all():
                comment.commentLikes.remove(logged_in_user_profile)
                logged_in_user_profile.num_of_likes = logged_in_user_profile.num_of_likes - 1
            else:
                comment.commentLikes.add(logged_in_user_profile)
                logged_in_user_profile.num_of_likes = logged_in_user_profile.num_of_likes + 1
        logged_in_user_profile.save()
        return redirect_url

class CommentVoteUp(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        
        if logged_in_user.is_authenticated:
            # if user has already voted down before pressing up, remove the vote down first 
            if logged_in_user_profile in comment.commentVotersDown.all():
                comment.commentVotersDown.remove(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1

            if logged_in_user_profile in comment.commentVotersUp.all():
                comment.commentVotersUp.remove(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1
            else:
                comment.commentVotersUp.add(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1
            comment.save()
        return redirect_url

class CommentVoteDown(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        
        if logged_in_user.is_authenticated:
            # if user has already voted up before pressing down, remove the vote up first 
            if logged_in_user_profile in comment.commentVotersUp.all():
                comment.commentVotersUp.remove(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1

            if logged_in_user_profile in comment.commentVotersDown.all():
                comment.commentVotersDown.remove(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes + 1
            else:
                comment.commentVotersDown.add(logged_in_user_profile)
                comment.commentNumberOfVotes = comment.commentNumberOfVotes - 1
            comment.save()
        return redirect_url

class CommentDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Comment 
    success_url = reverse_lazy('main:index')

    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments -= 1 # decrement 1 for this comment

        comment = self.get_object()
        
        # updating the likes count and the total num of posts/comments/replies count for each user who replied 
        replies_to_comment = comment.reply_set.all()
        for reply in replies_to_comment:
            post.postNumberOfComments -= 1 # decrement 1 for every reply to this comment
            reply_author_profile = UserProfile.objects.get(pk=reply.replyBy.pk)
            reply_author_profile.num_of_posts_comments_replies = reply_author_profile.num_of_posts_comments_replies - 1
            reply_author_profile.save()
            for user_profile in reply.replyLikes.all():
                profile = UserProfile.objects.get(pk=user_profile.pk)
                profile.num_of_likes = profile.num_of_likes - 1
                profile.save()

        author_profile = comment.commentBy
        author_profile.num_of_posts_comments_replies = author_profile.num_of_posts_comments_replies - 1

        # update the likes count for the comment author 
        if author_profile in comment.commentLikes.all():
            author_profile.num_of_likes = author_profile.num_of_likes - 1

        # update the likes count for each user that liked this comment. if the author has liked their own comment, it will be over written when we save author_profile
        for user_profile in comment.commentLikes.all():
            profile = UserProfile.objects.get(pk=user_profile.pk)
            profile.num_of_likes = profile.num_of_likes - 1
            profile.save()

        author_profile.save()
        
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
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            comment.commentFlags.add(logged_in_user_profile)
        return redirect_url


class CommentEnableDisablePage(generic.DeleteView):
    model = Comment
    template_name = 'main/flagged-posts/disable-comment.html'

class CommentEnableDisable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        comment.commentDisabled = not comment.commentDisabled
        comment.save()
        return redirect_url

class CommentRemoveFlagsPage(generic.DetailView):
    model = Comment 
    template_name = 'main/flagged-posts/remove-flags-comment.html'

class CommentRemoveFlags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        comment.commentFlags.clear()
        comment.commentNumberOfFlags = 0
        comment.commentDisabled = False
        comment.save()
        return redirect_url
