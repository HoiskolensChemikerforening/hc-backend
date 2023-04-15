from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Social, Bedpres
from .serializer import SocialSerializer, BedpresSerializer


class SocialListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SocialSerializer
    queryset = Social.objects.all()


class SocialDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Social.objects.all()
    serializer_class = SocialSerializer


class SocialUpcoming(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SocialSerializer
    queryset = Social.objects.filter(date__gte=timezone.now())


class MySocial(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # TODO: Only get previous events that the user has attended
    serializer_class = SocialSerializer
    queryset = Social.objects.filter(date__gte=timezone.now())


class BedpresListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Bedpres.objects.all()
    serializer_class = BedpresSerializer


class BedpresDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Bedpres.objects.all()
    serializer_class = BedpresSerializer


class BedpresUpcoming(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BedpresSerializer
    queryset = Bedpres.objects.filter(date__gte=timezone.now())


class MyBedpres(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # TODO: Only get previous events that the user has attended
    serializer_class = BedpresSerializer
    queryset = Bedpres.objects.filter(date__gte=timezone.now())
