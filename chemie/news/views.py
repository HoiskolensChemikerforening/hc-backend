from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from .models import Article
from .forms import ArticleForm
from .serializers import ArticleSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@permission_required("news.add_article")
def create_post(request):
    post = ArticleForm(request.POST or None, request.FILES or None)

    if request.POST:
        if post.is_valid():
            instance = post.save(commit=False)
            instance.author = request.user
            instance.save()

            # Check if removing this fixes the bug when posting a new article

            # subscriptions = Subscription.objects.filter(subscription_type=2)
            # subscribers = [sub.owner for sub in subscriptions]
            # instance.send_push(subscribers)
            return HttpResponseRedirect(reverse("news:index"))

    context = {"post": post}

    return render(request, "news/create_post.html", context)


def news_details(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    context = {"article": article}
    return render(request, "news/detail.html", context)


def list_all(request):
    all_posts = Article.objects.filter(published=True).order_by(
        "-published_date"
    )
    context = {"posts": all_posts}
    return render(request, "news/list.html", context)


@permission_required("news.delete_article")
def delete_article(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    messages.add_message(
        request, messages.SUCCESS, "Nyheten ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("news:index"))


@permission_required("news.change_article")
def edit_article(request, article_id, slug):
    article = get_object_or_404(Article, id=article_id)
    post = ArticleForm(
        request.POST or None, request.FILES or None, instance=article
    )
    if request.method == "POST":
        if post.is_valid():
            post.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Nyheten ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("news:index"))
    context = {"post": post}

    return render(request, "news/create_post.html", context)


class ListAllArticles(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Article.objects.filter(published=True).order_by("-id")
    serializer_class = ArticleSerializer


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
