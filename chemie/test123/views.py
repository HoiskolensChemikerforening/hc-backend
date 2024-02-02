from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

def testViews(request):
    liste = [1,2,3,4,5]
    context = {'liste':liste}
    return render(request, "index.html", context)