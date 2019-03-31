from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from post.models import Post
from reply.models import Reply
from .models import Comment
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from main.views import send_report_email_to_staff, send_report_email_to_author

# creates a comment 
class Comment_Create(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Comment 
    fields = ['commentContent']
    
    def form_valid(self, form):
        comment = form.save(commit=False) # don't save it in the database yet
        post = Post.objects.get(id=self.kwargs['pk'])
        if post.postClosed:
            return render(self.request, 'main/page-not-found.html')

        comment.commentOnPost = post
        logged_in_user = self.request.user        
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.numOfPostsCommentsReplies = user_profile.numOfPostsCommentsReplies + 1
        comment.commentBy = user_profile
        user_profile.save()
        return super(Comment_Create, self).form_valid(form)
    
    # sends an email to those who contributed on the post once the comment is successfully made
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        post.postNumberOfComments += 1
        
        logged_in_user = self.request.user

        subject = 'A New Comment! - Intelligent Q&A Forums'
        email_to = []
        # don't email yourself 
        if post.postedBy.user != logged_in_user:
            email_to.append(post.postedBy.user.email)
        # email every user that has commented on the post  
        for comment in post.comment_set.all():
            if comment.commentBy.user != logged_in_user:
                # don't email users who have commented twice more than once 
                if comment.commentBy.user.email not in email_to:
                    email_to.append(comment.commentBy.user.email)

        with open(settings.BASE_DIR + "/comment/templates/comment/notify_author_email.txt") as temp:
            notify_author_email = temp.read()
        email = EmailMultiAlternatives(
            subject=subject, 
            body=notify_author_email,
            from_email=settings.EMAIL_HOST_USER,
            to=email_to
        )
        html = get_template("comment/notify_author_email.html").render({'post': post, 'comment':self.object, 'comment_by':logged_in_user})
        email.attach_alternative(html, "text/html")
        email.send()

        post.save()

        return '/' + str(self.kwargs['pk'])

# updates a comment on a post 
class Comment_Update(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Comment
    template_name = 'comment/comment_edit_form.html'
    fields = ['commentContent']
    
    def get(self, request, *args, **kwargs):
        try:
            comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
            if (self.request.user == comment.commentBy.user):
                return super(Comment_Update, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author can edit
        except Http404:
            return HttpResponseRedirect("/page-not-found") # comment not available in database

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])

# like a comment 
class Comment_Like(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if logged_in_user_profile in comment.commentLikes.all():
                comment.commentLikes.remove(logged_in_user_profile)
                logged_in_user_profile.numberOfLikes = logged_in_user_profile.numberOfLikes - 1
            else:
                comment.commentLikes.add(logged_in_user_profile)
                logged_in_user_profile.numberOfLikes = logged_in_user_profile.numberOfLikes + 1
        logged_in_user_profile.save()
        return redirect_url

# shows a list of users who like a specific comment 
class Comment_Likes_List(generic.DetailView):
    model = Comment 
    template_name = 'comment/comment-likes-list.html'
    def get_context_data(self, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        list_of_users = [] 
        for username in comment.commentLikes.all():
            user = get_object_or_404(User, username=username)
            list_of_users.append(user)
        return {'comment': comment, 'list_of_users': list_of_users}

# adds a vote up on a comment 
class Comment_Vote_Up(RedirectView):
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

# adds a vote down on a comment 
class Comment_Vote_Down(RedirectView):
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

# deletes a comment and all replies to that comment
class Comment_Delete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Comment 
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        try:
            comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
            if (self.request.user == comment.commentBy.user or self.request.user.is_staff):
                return super(Comment_Delete, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author or staff can delete
        except Http404:
            return HttpResponseRedirect("/page-not-found") # comment not available in database

    # changes the likes counts and total number of posts for users involved 
    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        post.postNumberOfComments -= 1 # decrement 1 for this comment

        comment = self.get_object()
        
        # updating the likes count and the total num of posts/comments/replies count for each user who replied 
        replies_to_comment = comment.reply_set.all()
        for reply in replies_to_comment:
            post.postNumberOfComments -= 1 # decrement 1 for every reply to this comment
            reply_author_profile = UserProfile.objects.get(pk=reply.replyBy.pk)
            reply_author_profile.numOfPostsCommentsReplies = reply_author_profile.numOfPostsCommentsReplies - 1
            reply_author_profile.save()
            for user_profile in reply.replyLikes.all():
                profile = UserProfile.objects.get(pk=user_profile.pk)
                profile.numberOfLikes = profile.numberOfLikes - 1
                profile.save()

        author_profile = comment.commentBy
        author_profile.numOfPostsCommentsReplies = author_profile.numOfPostsCommentsReplies - 1

        # update the likes count for the comment author 
        if author_profile in comment.commentLikes.all():
            author_profile.numberOfLikes = author_profile.numberOfLikes - 1

        # update the likes count for each user that liked this comment. if the author has liked their own comment, it will be over written when we save author_profile
        for user_profile in comment.commentLikes.all():
            profile = UserProfile.objects.get(pk=user_profile.pk)
            profile.numberOfLikes = profile.numberOfLikes - 1
            profile.save()

        author_profile.save()
        
        post.save()
        comment.delete()
        return HttpResponseRedirect(self.get_success_url())

    # context data needed in the html 
    def get_context_data(self, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        return {'post_pk': self.kwargs['post_pk'], 'comment': comment}

    def get_success_url(self):
        return '/' + str(self.kwargs['post_pk'])
    
# reports a comment and notifies all staff members via email
class Comment_Report(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        if logged_in_user.is_authenticated:
            logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
            if logged_in_user_profile not in comment.commentFlags.all(): # disallows the same user to notify staff twice on the same comment
                comment.commentFlags.add(logged_in_user_profile)

                send_report_email_to_staff(
                    discussion_type = 'comment',
                    discussion = comment.commentContent, 
                    discussion_by = comment.commentBy,
                    logged_in_user = logged_in_user
                )
                send_report_email_to_author(
                    discussion_type = 'comment',
                    discussion = comment.commentContent, 
                    discussion_by = comment.commentBy,
                )

        else:
            return redirect('/page-not-found')
        return redirect_url

# prompts the user to confirm they want to disable/enable a comment on a post 
class Comment_Enable_Disable_Page(generic.DeleteView):
    model = Comment
    template_name = 'main/flagged-posts/disable-comment.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Comment_Enable_Disable_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')
        
# enables and disables a comment 
class Comment_Enable_Disable(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
            comment.commentDisabled = not comment.commentDisabled
            comment.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')

# prompts the user to confirm they want to remove flags from a comment
class Comment_Remove_Flags_Page(generic.DetailView):
    model = Comment 
    template_name = 'main/flagged-posts/remove-flags-comment.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Comment_Remove_Flags_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')

# removes flags (reports) from a comment 
class Comment_Remove_Flags(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
            comment.commentFlags.clear()
            comment.commentDisabled = False
            comment.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')

# accepts a comment as an answer to the post 
class Accept_Answer(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))        
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        if comment.commentBy == post.postedBy: 
            return redirect('/page-not-found') # you cannot accept your comment on your own post
        logged_in_user = self.request.user    
        if logged_in_user == post.postedBy.user:
            comment.commentAccepted = True 
            post.postClosed = True 
        else:
            return redirect('/page-not-found') # you cannot accept an answer if you're not the post owner
        comment.save()
        post.save()
        return redirect('/' + str(post.pk))
        