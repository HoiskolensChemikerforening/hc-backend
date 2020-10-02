from django.shortcuts import render
from .forms import PodcastForm
from .models import Podcast
from django.contrib import messages
from chemie.web_push.models import Subscription
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
)
from django.views.generic.edit import (
    DeleteView,
)
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

class ListPodcastDeleteView(PermissionRequiredMixin, ListView):
    template_name = "sugepodden/delete.html"
    permission_required = "sugepodden.delete_podcast"
    model = Podcast

    def queryset(self):
        return self.model.objects.filter(
             published=True
        )


class DeletePodcastView(PermissionRequiredMixin, DeleteView):
    model = Podcast
    permission_required = "sugepodden.delete_podcast"
    success_url = reverse_lazy("sugepodden:delete_list_podcast")

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.published = False
        object.save()
        messages.add_message(
            request,
            messages.WARNING,
            "Podcasten ble slettet",
            extra_tags="Slettet",
        )
        return HttpResponseRedirect(self.success_url)


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
def delete_podcast(request, Podcast_id):
    podcast = get_object_or_404(Podcast, id=Podcast_id)
    podcast.published = False
    podcast.save()
    messages.add_message(
        request, messages.SUCCESS, "Podcasten ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("sugepodden:delete_list_podcast"))

def list_all(request):

    all_posts = Podcast.objects.filter(published=True).order_by(
        "-published_date"
    )
    context = {"posts": all_posts}
    return render(request, "sugepodden/list.html", context)

@permission_required("news.change_article")
def edit_podcast(request, podcast_id, slug):
    podcast = get_object_or_404(Podcast, id=podcast_id)
    post = PodcastForm(
        request.POST or None, request.FILES or None, instance=podcast
    )
    if request.method == "POST":
        if post.is_valid():
            post.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Podcasten ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("podcast:index"))
    context = {"post": post}

    return render(request, "podcast/create_post.html", context)
