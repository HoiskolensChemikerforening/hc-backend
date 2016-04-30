from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from .models import NewsPost

def index(request):
    all_posts = NewsPost.objects.all()
    for post in all_posts:
        print(post.content)
    context = {
            'newsposts': all_posts
    }
    return render(request,'news/detail.html', context)
