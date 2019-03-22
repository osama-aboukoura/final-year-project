from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from post.models import Post
from comment.models import Comment
from .models import Reply
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from main.views import send_report_email_to_staff


# creates a reply and emails everyone who replied to the same comment and the comment and post author
class Reply_Create(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Reply 
    fields = ['replyContent']
    
    def form_valid(self, form):
        reply = form.save(commit=False) # don't save it in the database yet
        comment = Comment.objects.get(id=self.kwargs['comment_pk'])
        post = Post.objects.get(id=self.kwargs['post_pk'])
        if post.postClosed:
            return render(self.request, 'main/page-not-found.html')
        reply.replytoComment = comment
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.numOfPostsCommentsReplies = user_profile.numOfPostsCommentsReplies + 1
        reply.replyBy = user_profile
        user_profile.save()
        return super(Reply_Create, self).form_valid(form)
    
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

# updates a reply to a comment after authenticating the user 
class Reply_Update(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Reply
    template_name = 'reply/reply_edit_form.html'
    fields = ['replyContent']

    def get(self, request, *args, **kwargs):
        try:
            reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
            if (self.request.user == reply.replyBy.user):
                return super(Reply_Update, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author can edit
        except Http404:
            return HttpResponseRedirect("/page-not-found") # reply not available in database

    # send the user back to the post page after updating the reply 
    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    
# like a reply and change the total number of likes the user has made 
class Reply_Like(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if logged_in_user_profile in reply.replyLikes.all():
                reply.replyLikes.remove(logged_in_user_profile)
                logged_in_user_profile.numberOfLikes = logged_in_user_profile.numberOfLikes - 1
            else:
                reply.replyLikes.add(logged_in_user_profile)
                logged_in_user_profile.numberOfLikes = logged_in_user_profile.numberOfLikes + 1
        logged_in_user_profile.save()
        return redirect_url

# shows a list of users who liked a reply 
class Reply_Likes_List(generic.DetailView):
    model = Reply 
    template_name = 'reply/reply-likes-list.html'
    def get_context_data(self, **kwargs):
        reply = Reply.objects.get(id=self.kwargs['pk'])
        list_of_users = [] 
        for username in reply.replyLikes.all():
            user = get_object_or_404(User, username=username)
            list_of_users.append(user)
        return {'reply': reply, 'list_of_users': list_of_users}

# deletes a reply and updates the likes count and total number of posts of all involved users 
class Reply_Delete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Reply 
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        try:
            reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
            if (self.request.user == reply.replyBy.user or self.request.user.is_staff):
                return super(Reply_Delete, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author or staff can delete
        except Http404:
            return HttpResponseRedirect("/page-not-found") # reply not available in database


    def delete(self, request, *args, **kwargs):
        reply = self.get_object()
        author_profile = reply.replyBy
        author_profile.numOfPostsCommentsReplies = author_profile.numOfPostsCommentsReplies - 1
        
        # update the likes count for the reply author 
        if author_profile in reply.replyLikes.all():
            author_profile.numberOfLikes = author_profile.numberOfLikes - 1

        # update the likes count for each user that liked this reply. if the author has liked their own reply, it will be over written when we save author_profile
        for user_profile in reply.replyLikes.all():
            profile = UserProfile.objects.get(pk=user_profile.pk)
            profile.numberOfLikes = profile.numberOfLikes - 1
            profile.save()

        author_profile.save()
        reply.delete()
        return HttpResponseRedirect(self.get_success_url())

    # context data needed in the html 
    def get_context_data(self, **kwargs):
        reply = Reply.objects.get(id=self.kwargs['pk'])
        return {'post_pk': self.kwargs['post_pk'], 'reply': reply}

    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments -= 1
        post.save()
        return '/' + str(self.kwargs['post_pk'])

# reports a reply and notifies all staff members via email
class Reply_Report(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if logged_in_user_profile not in reply.replyFlags.all(): # disallows the same user to notify staff twice on the same reply
                reply.replyFlags.add(logged_in_user_profile)

                send_report_email_to_staff(
                    discussion_type = 'reply',
                    discussion = reply.replyContent, 
                    discussion_by = reply.replyBy,
                    logged_in_user = logged_in_user
                )

        else:
            return redirect('/page-not-found')
        return redirect_url

# prompts the user to confirm they want to disable/enable a reply on a comment 
class Reply_Enable_Disable_Page(generic.DeleteView):
    model = Reply
    template_name = 'main/flagged-posts/disable-reply.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Reply_Enable_Disable_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')

# enables and disables a reply 
class Reply_Enable_Disable(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
            reply.replyDisabled = not reply.replyDisabled
            reply.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')

# prompts the user to confirm they want to remove flags from a reply
class Reply_Remove_Flags_Page(generic.DetailView):
    model = Reply 
    template_name = 'main/flagged-posts/remove-flags-reply.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Reply_Remove_Flags_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')

# removes flags (reports) from a reply 
class Reply_Remove_Flags(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            reply = get_object_or_404(Reply, id=self.kwargs.get('pk'))
            reply.replyFlags.clear()
            reply.replyDisabled = False
            reply.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')
