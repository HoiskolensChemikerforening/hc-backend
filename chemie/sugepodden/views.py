from django.shortcuts import render

from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponse

from .models import Podcast
from .forms import PodcastForm
#LEGG INN PERMISSION <3

def index(request):
  return HttpResponse("Hello World!")


def create_post(request):
    post = PodcastForm(request.POST or None, request.FILES or None)
    if post.is_valid():
        instance = post.save(commit=False)
        instance.author = request.user

        return HttpResponseRedirect("sugepodden:index")
    context = {"post" : post}
    return render(request, "sugepodden/create_podcast.html", context)