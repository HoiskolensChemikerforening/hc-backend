from django.shortcuts import get_object_or_404, render
from .models import Article
from .forms import NewsForm


def index(request):
    all_articles = Article.objects.all()
    context = {
        'articles': all_articles
    }
    return render(request, 'news/overview.html', context)


def display_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article
    }
    return render(request, 'news/single.html', context)


def create_article(request):
    post = NewsForm(request.POST or None)
    if post.is_valid():
        post.save()
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


def edit_article(request, pk):
    pass


def delete_article(request, pk):
    pass
