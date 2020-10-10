from .forms import PodcastForm
from .models import Podcast
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.list import ListView


class ListPodcastDeleteView(PermissionRequiredMixin, ListView):
    template_name = "sugepodden/delete.html"
    permission_required = "sugepodden.delete_podcast"
    model = Podcast

    def queryset(self):
        return self.model.objects.filter(published=True)


@permission_required("sugepodden.add_podcast")
def create_podcast(request):
    post = PodcastForm(request.POST or None, request.FILES or None)
    if request.POST:
        if post.is_valid():
            instance = post.save(commit=False)
            instance.author = request.user
            instance.save()

            return HttpResponseRedirect(reverse("sugepodden:index"))
    context = {"post": post}
    return render(request, "sugepodden/create_podcast.html", context)


@permission_required("sugepodden.delete_podcast")
def delete_podcast(request, pk):
    podcast = get_object_or_404(Podcast, id=pk)
    podcast.published = False
    podcast.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        "Podcasten ble slettet",
        extra_tags="Slettet",
    )
    return HttpResponseRedirect(reverse("sugepodden:delete_list_podcast"))


def list_all(request):

    all_posts = Podcast.objects.filter(published=True).order_by(
        "-published_date"
    )
    context = {"posts": all_posts}
    return render(request, "sugepodden/list.html", context)
