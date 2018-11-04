from django.shortcuts import render, get_object_or_404
from .models import Post

def index (request):
    all_posts = Post.objects.all()
    return render(request, 'post/index.html', { 'all_posts': all_posts })

def showPost (request, post_id):
    #post = Post.objects.get(pk=post_id)
    post = get_object_or_404(Post, pk=post_id)
    date = getFormattedDateAndTime(post.postDate) 
    return render(request, 'post/singlePost.html', { 'post': post, 'date': date })


def getFormattedDateAndTime(date):
    formattedDate = date.strftime("%B") + " " + str(date.strftime("%d")) + ", " + date.strftime("%Y")
    formattedDate += ' at ' + date.strftime("%H:%M")
    return formattedDate
