from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World!")


'''
def create_post(request):
    post = PodcastForm(request.POST or None, request.FILES or None)
    if post.is_valid():
        instance = post.save(commit=False)
        instance.author = request.user

        return HttpResponseRedirect("sugepodden:index")
    context = {"post": post}
    return render(request, "sugepodden/create_podcast.html", context)
'''
