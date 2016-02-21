from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .shitbox import Post

def get_name(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if (is_valid(form)):
            return HttpResponseRedirect('/Takk/')
    else:
        form = Post()
