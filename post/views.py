from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Comment, Reply
from django.urls import reverse
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all()

class ShowPostView(generic.DetailView):
    model = Post 
    template_name = 'post/post-comment-reply.html'


class PostCreate(CreateView):
    model = Post 
    fields = ['postedBy', 'postTitle', 'postTopic', 'postContent']

class PostUpdate(UpdateView):
    model = Post 
    template_name = 'post/post_edit_form.html'
    fields = ['postedBy', 'postTitle', 'postTopic', 'postContent']

class PostDelete(DeleteView):
    model = Post 
    success_url = reverse_lazy('post:index')


class CommentCreate(CreateView):
    model = Comment 
    fields = ['commentBy', 'commentContent']
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment.commentOnPost = post
        return super(CommentCreate, self).form_valid(form)
    
    def get_success_url(self):
        return '/posts/' + str(self.kwargs['pk'])

class CommentUpdate(UpdateView):
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Comment
    template_name = 'post/comment_edit_form.html'
    fields = ['commentBy','commentContent']

    def get_success_url(self):
        return '/posts/' + str(self.kwargs['post_pk'])

class CommentDelete(DeleteView):
    model = Comment 

    def get_success_url(self):
        return '/posts/' + str(self.kwargs['post_pk'])

class ReplyCreate(CreateView):
    model = Reply 
    fields = ['replyBy', 'replyContent']
    
    def form_valid(self, form):
        reply = form.save(commit=False)
        comment = Comment.objects.get(id=self.kwargs['comment_pk'])
        reply.replytoComment = comment
        return super(ReplyCreate, self).form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['post_pk'])
        return '/posts/' + str(post.pk)

class ReplyUpdate(UpdateView):
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    model = Reply
    template_name = 'post/reply_edit_form.html'
    fields = ['replyBy','replyContent']

    def get_success_url(self):
        return '/posts/' + str(self.kwargs['post_pk'])
    
class ReplyDelete(DeleteView):
    model = Reply 
    
    def get_success_url(self):
        return '/posts/' + str(self.kwargs['post_pk'])
