from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from .models import Article
from .forms import NewsPost


@permission_required('news.add_article')
def create_post(request):
    post = NewsPost(request.POST or None, request.FILES or None)
    if request.POST:
        if post.is_valid():
            instance = post.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.add_message(request, messages.WARNING, 'Nyheten ble opprettet', extra_tags='Opprettet')
            return HttpResponseRedirect(reverse('news:index'))
    context = {
        'post': post
    }
    return render(request, 'news/create_post.html', context)


def news_details(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    context = {
        'article': article
    }
    return render(request, 'news/detail.html', context)


def list_all(request):
    all_posts = Article.objects.filter(published=True).order_by('-published_date')
    context = {
        'posts': all_posts,
    }
    return render(request, 'news/list.html', context)

@permission_required("news.delete_article")
def list_article_delete(request):
    all_posts = Article.objects.filter(published=True).order_by('-published_date')
    context = {
        'posts': all_posts,
    }
    return render(request, 'news/list_delete.html', context)

@permission_required("news.delete_article")
def delete_article(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    article.published = False
    article.save()
    messages.add_message(request, messages.WARNING, 'Nyheten ble slettet', extra_tags='Slettet')
    return HttpResponseRedirect(reverse("news:index"))

@permission_required("news.change_article")
def edit_article(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        post = NewsPost(request.POST, instance=article)
        try:
            if post.is_valid():
                post.save()
                messages.add_message(request, messages.WARNING, 'Nyheten ble endret', extra_tags='Endret')
                return HttpResponseRedirect(reverse('news:index'))
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'Nyheten ble ikke endret på grunn av et problem: {}'.format(e), extra_tags='Feil')
    else:
        post = NewsPost(instance=article)
    context = {
        'post': post,
    }
    return render(request, 'news/create_post.html', context)