from random import choice

from django.shortcuts import render

from .models import pictures_for_404


def page_not_found(request, exception):
    img_404 = pictures_for_404.objects.all()
    try:
        random_image = choice(img_404)
    except IndexError:
        random_image = None

    return render(
        request, "404.html", context={"image": random_image}, status=404
    )
