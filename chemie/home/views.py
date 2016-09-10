from django.shortcuts import render
from django.template import RequestContext
from events.models import Event
from news.models import Article
from django.utils import timezone

def index(request):
    all_events = Event.objects.filter(date__gt=timezone.now())
    all_posts = Article.objects.all()
    context = {
        'events': all_events,
        'posts': all_posts,
    }
    return render(request, 'home/index.html', context)