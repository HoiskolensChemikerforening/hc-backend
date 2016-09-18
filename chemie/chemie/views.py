from random import choice
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from .models import pictures_for_404


def show_404(request):
    img_404 = pictures_for_404.objects.all()
    rand_img = choice(img_404)

    return render(request, 'chemie/404.html', context={'bilde':rand_img}, status=404)