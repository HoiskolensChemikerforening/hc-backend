from django.shortcuts import render, redirect
from django.contrib.auth.models import User


from .models import Article
from .forms import NewsPost

def create_post(request):
    post = NewsPost(request.POST or None)
    if request.POST:
        instance = post.save(commit=False)
        instance.author = request.user
        instance.save()

    context = {
        'post': post
    }
    return render(request, 'news/create_post.html', context)

def news_details(request, article_id):
    article = Article.objects.get(year__gt=datetime.now())

def list_all(request):
    all_posts = Article.objects.all()
    context = {
        'posts': all_posts,
    }
    return render(request, 'news/list_all', context)