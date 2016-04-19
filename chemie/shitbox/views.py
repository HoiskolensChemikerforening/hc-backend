from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import Postform


def post_votes(request):
    form = Postform(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
    context = {
        "form": form,
    }
    return render(request, "shitbox/post_form.html", context)
