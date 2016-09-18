from random import choice
from django.shortcuts import render
from .models import pictures_for_404


def show_404(request):
    img_404 = pictures_for_404.objects.all()
    try:
        random_image = choice(img_404)
    except IndexError:
        random_image = None

    return render(request, 'chemie/404.html', context={'bilde': random_image}, status=404)
