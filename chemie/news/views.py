from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from .models import Article
from .forms import Newsform

def index(request):
    all_articles = Article.objects.all()
    for post in all_articles:
        context = {
            'articles': all_articles
            }
    return render(request,'news/detail.html', context)

def display_article(request, slug):
    article = Article.objects.all()
    context = {
        'article': article
    }
    return render(request, 'news/single.html', context)

def create_article(request):
    post = Newsform(request.POST or None)
    if post.is_valid():
        news = post.save()
        context = {
            "title": 'Fullført',
            "message": 'Artikkelen har blitt postet.',
            "status": 'success',
        }
        return render(request, 'common/feedback.html', context)
    context = {
        "post": post,
    }
    return render(request, 'news/administrer.html', context)
