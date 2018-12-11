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
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template



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

        reply = self.object 
        comment = reply.replytoComment

        logged_in_user = self.request.user

        subject = 'A New Reply! - Intelligent Q&A Forums'
        email_to = []
        # email the post author if it isn't yourself 
        if post.postedBy.user != logged_in_user:
            email_to.append(post.postedBy.user.email)
        # email the comment author if it isn't yourself 
        if comment.commentBy.user != logged_in_user:
            if comment.commentBy.user.email not in email_to:
                email_to.append(comment.commentBy.user.email)
        # email every user that has replied to the comment  
        for reply in comment.reply_set.all():
            if reply.replyBy.user != logged_in_user:
                # don't email users who have replied twice more than once 
                if reply.replyBy.user.email not in email_to:
                    email_to.append(reply.replyBy.user.email)

        with open(settings.BASE_DIR + "/reply/templates/reply/notify_author_email.txt") as temp:
            notify_author_email = temp.read()
        email = EmailMultiAlternatives(
            subject=subject, 
            body=notify_author_email,
            from_email=settings.EMAIL_HOST_USER,
            to=email_to
        )
        html = get_template("reply/notify_author_email.html").render({'post': post, 'comment':comment, 'reply':self.object, 'reply_by':logged_in_user})
        email.attach_alternative(html, "text/html")
        email.send()

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
        reply = self.get_object()
        author_profile = reply.replyBy
        author_profile.num_of_posts_comments_replies = author_profile.num_of_posts_comments_replies - 1
        
        # update the likes count for the reply author 
        if author_profile in reply.replyLikes.all():
            author_profile.num_of_likes = author_profile.num_of_likes - 1

        # update the likes count for each user that liked this reply. if the author has liked their own reply, it will be over written when we save author_profile
        for user_profile in reply.replyLikes.all():
            profile = UserProfile.objects.get(pk=user_profile.pk)
            profile.num_of_likes = profile.num_of_likes - 1
            profile.save()

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