from random import choice
from django.shortcuts import render
from .models import pictures_for_404

from django.contrib.auth.models import User
from rest_framework import viewsets, response, permissions
from .serializers import UserSerializer


def page_not_found(request, exception):
    img_404 = pictures_for_404.objects.all()
    try:
        random_image = choice(img_404)
    except IndexError:
        random_image = None

    return render(
        request, "404.html", context={"image": random_image}, status=404
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                                                    context={'request': request}).data)
        return super(UserViewSet, self).retrieve(request, pk)
