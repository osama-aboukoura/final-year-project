from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from main.models import UserProfile, User
from .models import Post
from comment.models import Comment
from reply.models import Reply
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from .nmf import classify_post_topics
from main.views import send_report_email_to_staff, send_report_email_to_author


# shows a post only if it's not disabled 
class Show_Post_View(generic.DetailView):
    model = Post 
    template_name = 'post/post-comment-reply.html'
    def get(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        try:
            post = get_object_or_404(Post, id=self.kwargs.get('pk'))

            # only staff and admin can view disabled posts 
            if (post.postDisabled and not logged_in_user.is_staff):
                return HttpResponseRedirect("/page-not-found") 
                
        except Http404:
            return HttpResponseRedirect("/page-not-found") # post not available in database

        try:
            return super(Show_Post_View, self).get(request, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect("/page-not-found")
    
    # context data needed for the template 
    def get_context_data(self, **kwargs):
        context = super(Show_Post_View, self).get_context_data(**kwargs)
        logged_in_user = self.request.user
        if logged_in_user.is_authenticated:
            logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
            context['logged_in_user_profile'] = logged_in_user_profile
        context['postTopicNoSpaces'] = self.object.postTopic.replace(" ", "")
        return context

# creates a post and allows classification either automatically or manually 
class Post_Create(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post 
    fields = ['postTitle', 'postTopic', 'postContent', 'postImage']

    # always runs before the form_valid function 
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        postTitle = self.request.POST.get('postTitle')
        postTopic = self.request.POST.get('postTopic')
        postContent = self.request.POST.get('postContent')
        checkbox  = self.request.POST.get('postAutoClassification')

        if (postTopic == "" and checkbox != "on"):
            form.add_error('postTopic', 'Error') # making the form invalid 
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, "Error: Either tick the checkbox to automatically classify "
                            + "the topic of the post, or manually fill out the 'Post Topic' field.")
            return render(request, "post/post_form.html", {'postTitle': postTitle, 'postContent': postContent})

    def form_valid(self, form):
        self.object = form.save(commit=False) # don't save it in the database yet
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.numOfPostsCommentsReplies = user_profile.numOfPostsCommentsReplies + 1
        self.object.postedBy = user_profile
        checkbox = self.request.POST.get('postAutoClassification')
        if (checkbox == "on"):
            self.object.postAutoClassification = True

            # the post to classify is the title plus the content to get as much info as possible 
            postToAutoClassify = str(self.object.postTitle) + " " + str(self.object.postContent)
            
            # calling the classifying algorithm 
            topic = classify_post_topics(postToAutoClassify)

            self.object.postTopic = topic.topicName
            self.object.postTopicRelatedWords = topic.topicWords

        if 'postImage' in self.request.POST:
            self.object.postImage = self.request.POST.get('postImage')

        user_profile.save()
        return super(Post_Create, self).form_valid(form)

# updates a post after authenticating the user 
class Post_Update(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post 
    template_name = 'post/post_edit_form.html'
    fields = ['postTitle', 'postTopic', 'postTopicRelatedWords', 'postContent', 'postImage']
    def get(self, request, *args, **kwargs):
        try:
            post = get_object_or_404(Post, id=self.kwargs.get('pk'))
            if (self.request.user == post.postedBy.user):
                return super(Post_Update, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author can edit
        except Http404:
            return HttpResponseRedirect("/page-not-found") # post not available in database
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'postImage' in request.FILES:
            self.object.postImage = request.FILES['postImage']
        return super().post(request, *args, **kwargs)

# likes a post 
class Post_Like(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()        
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            if user_profile in post.postLikes.all():
                post.postLikes.remove(user_profile)
                user_profile.numberOfLikes = user_profile.numberOfLikes - 1
            else:
                post.postLikes.add(user_profile)
                user_profile.numberOfLikes = user_profile.numberOfLikes + 1
        
        user_profile.save()
        return redirect_url

# shows a list of users who liked a post 
class Post_Likes_List(generic.DetailView):
    model = Post 
    template_name = 'post/post-likes-list.html'
    def get_context_data(self, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        list_of_users = [] 
        for username in post.postLikes.all():
            user = get_object_or_404(User, username=username)
            list_of_users.append(user)
        return {'post': post, 'list_of_users': list_of_users}

# adds a vote up to the post 
class Post_Vote_Up(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
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

# adds a vote down to the post 
class Post_Vote_Down(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
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

# deletes a post and all the comments and replies related 
class Post_Delete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post 

    def get(self, request, *args, **kwargs):
        try:
            post = get_object_or_404(Post, id=self.kwargs.get('pk'))
            if (self.request.user == post.postedBy.user or self.request.user.is_staff):
                return super(Post_Delete, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/page-not-found") # only author or staff can delete
        except Http404:
            return HttpResponseRedirect("/page-not-found") # post not available in database

    def get_success_url(self):
        return reverse_lazy('main:index')

    # updating the likes counts and total number of posts for all users involved 
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        post_author_profile = post.postedBy

        author_likes_to_delete = 0
        author_posts_to_delete = 1

        # update the likes count for the post author 
        if post_author_profile in post.postLikes.all():
            author_likes_to_delete += 1

        # update the likes count for everyone else who liked the post 
        for user_profile in post.postLikes.all():
            if post.postedBy != user_profile:
                profile = UserProfile.objects.get(pk=user_profile.pk)
                profile.numberOfLikes = profile.numberOfLikes - 1
                profile.save()

        comments_on_post = post.comment_set.all()
        for comment in comments_on_post:
            comment_author_profile = UserProfile.objects.get(pk=comment.commentBy.pk)
            if comment_author_profile == post_author_profile:
                author_posts_to_delete += 1
            else:
                comment_author_profile.numOfPostsCommentsReplies = comment_author_profile.numOfPostsCommentsReplies - 1
                comment_author_profile.save()
            # update the likes count for the list of people who liked this comment
            for user_profile in comment.commentLikes.all():
                profile = UserProfile.objects.get(pk=user_profile.pk)
                if user_profile == post_author_profile:
                    author_likes_to_delete += 1
                else:
                    profile.numberOfLikes = profile.numberOfLikes - 1
                    profile.save()
            # update the likes count for the list of people who liked the replies on this comment
            replies_to_comment = comment.reply_set.all()
            for reply in replies_to_comment:
                reply_author_profile = UserProfile.objects.get(pk=reply.replyBy.pk)
                if reply_author_profile == post_author_profile:
                    author_posts_to_delete += 1
                else:
                    reply_author_profile.numOfPostsCommentsReplies = reply_author_profile.numOfPostsCommentsReplies - 1
                    reply_author_profile.save()
                for user_profile_reply in reply.replyLikes.all():
                    profile_reply = UserProfile.objects.get(pk=user_profile_reply.pk)
                    if profile_reply == post_author_profile:
                        author_likes_to_delete += 1
                    else:
                        profile_reply.numberOfLikes = profile_reply.numberOfLikes - 1
                        profile_reply.save()
                
        post_author_profile.numOfPostsCommentsReplies = post_author_profile.numOfPostsCommentsReplies - author_posts_to_delete
        post_author_profile.numberOfLikes = post_author_profile.numberOfLikes - author_likes_to_delete

        post_author_profile.save()
        post.delete()
        return HttpResponseRedirect(self.get_success_url())
        
# reports a post and notifies all staff members via email
class Post_Report(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        if logged_in_user.is_authenticated:
            logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
            if logged_in_user_profile not in post.postFlags.all(): # disallows the same user to notify staff twice on the same post
                post.postFlags.add(logged_in_user_profile)

                send_report_email_to_staff(
                    discussion_type = 'post',
                    discussion = post.postContent, 
                    discussion_by = post.postedBy,
                    logged_in_user = logged_in_user
                )
                send_report_email_to_author(
                    discussion_type = 'post',
                    discussion = post.postContent, 
                    discussion_by = post.postedBy,
                )
                
        else:
            return redirect('/page-not-found')
        return redirect_url

# prompts the user to confirm they want to disable/enable a post 
class Post_Enable_Disable_Page(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/disable-post.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Post_Enable_Disable_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')

# enables and disables a post 
class Post_Enable_Disable(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            post = get_object_or_404(Post, id=self.kwargs.get('pk'))
            post.postDisabled = not post.postDisabled
            post.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')

# prompts the user to confirm they want to remove flags from a post
class Post_Remove_Flags_Page(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/remove-flags-post.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(Post_Remove_Flags_Page, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/page-not-found')

# removes flags (reports) from a post 
class Post_Remove_Flags(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            post = get_object_or_404(Post, id=self.kwargs.get('pk'))
            post.postFlags.clear()
            post.postDisabled = False
            post.save()
            return redirect('/flagged-posts')
        else:
            return redirect('/page-not-found')

# resests the accepted comment on the post and allows the post owner to accept a different answer
class Post_Open_Comments(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user    
        if logged_in_user == post.postedBy.user:
            post.postClosed = False
            for comment in post.comment_set.all():
                comment.commentAccepted = False
                comment.save() 
        post.save()
        return redirect_url
    