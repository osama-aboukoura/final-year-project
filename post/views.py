from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Comment, Reply
from django.urls import reverse

class IndexView(generic.ListView):
    template_name = 'post/index.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.all()

class ShowPostView(generic.DetailView):
    model = Post 
    template_name = 'post/singlePost.html'


class PostCreate(CreateView):
    model = Post 
    fields = ['postedBy', 'postTitle', 'postTopic', 'postContent']

class CommentCreate(CreateView):
    model = Comment 
    fields = ['commentBy', 'commentContent']
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        post = Post.objects.get(id=self.kwargs['pk'])
        comment.commentOnPost = post
        return super(CommentCreate, self).form_valid(form)
    
    def get_success_url(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        return '/posts/' + str(post.pk)

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

    

# def index (request):
#     all_posts = Post.objects.all()
#     return render(request, 'post/index.html', { 'all_posts': all_posts })

# def showPost (request, post_id):
#     #post = Post.objects.get(pk=post_id)
#     post = get_object_or_404(Post, pk=post_id)
#     date = getFormattedDateAndTime(post.postDate) 
#     return render(request, 'post/singlePost.html', { 'post': post, 'date': date })


# def getFormattedDateAndTime(date):
#     formattedDate = date.strftime("%B") + " " + str(date.strftime("%d")) + ", " + date.strftime("%Y")
#     formattedDate += ' at ' + date.strftime("%H:%M")
#     return formattedDate
