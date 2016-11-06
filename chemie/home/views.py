from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from news.models import Article


def index(request):
    all_events = Event.objects.filter(date__gt=timezone.now())
    all_posts = Article.objects.all()
    context = {
        'events': all_events,
        'posts': all_posts,
    }
    return render(request, 'chemie/index.html', context)
