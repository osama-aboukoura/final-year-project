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


class Show_Post_View(generic.DetailView):
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
#         return Post_Create.as_view()(request)
#     else:
#         return HttpResponseRedirect(reverse('post:user-login'))

class Post_Create(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Post 
    fields = ['postTitle', 'postTopic', 'postContent']
    
    def form_valid(self, form):
        post = form.save(commit=False)
        logged_in_user = self.request.user
        user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        user_profile.numOfPostsCommentsReplies = user_profile.numOfPostsCommentsReplies + 1
        post.postedBy = user_profile
        user_profile.save()
        return super(Post_Create, self).form_valid(form)

class Post_Update(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Post 
    template_name = 'post/post_edit_form.html'
    fields = ['postTitle', 'postTopic', 'postContent']

class Post_Like(RedirectView):
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

class Post_Vote_Up(RedirectView):
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

class Post_Vote_Down(RedirectView):
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

class Post_Delete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Post 

    def get_success_url(self):
        return reverse_lazy('main:index')

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
        
class Post_Report(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = post.get_absolute_url()
        logged_in_user = self.request.user 
        logged_in_user_profile = get_object_or_404(UserProfile, user=logged_in_user)
        if logged_in_user.is_authenticated:
            post.postFlags.add(logged_in_user_profile)
        return redirect_url

class Post_Enable_Disable_Page(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/disable-post.html'

class Post_Enable_Disable(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        post.postDisabled = not post.postDisabled
        post.save()
        return redirect_url

class Post_Remove_Flags_Page(generic.DetailView):
    model = Post 
    template_name = 'main/flagged-posts/remove-flags-post.html'

class Post_Remove_Flags(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        redirect_url = '/flagged-posts/'
        post.postFlags.clear()
        post.postNumberOfFlags = 0
        post.postDisabled = False
        post.save()
        return redirect_url

