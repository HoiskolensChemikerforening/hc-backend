from random import choice

from django.shortcuts import render
from rest_framework import generics

from .models import pictures_for_404, Sponsor
from .serializer import pictures_for_404Serializer, SponsorSerializer


def page_not_found(request, exception):
    img_404 = pictures_for_404.objects.all()
    try:
        random_image = choice(img_404)
    except IndexError:
        random_image = None

    return render(
        request, "404.html", context={"image": random_image}, status=404
    )


class pictures_for_404ListCreate(generics.ListCreateAPIView):
    queryset = pictures_for_404.objects.all()
    serializer_class = pictures_for_404Serializer


class SponsorListCreate(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class pictures_for_404Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = pictures_for_404.objects.all()
    serializer_class = pictures_for_404Serializer


class SponsorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
