from django.shortcuts import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, welcome to stock app. Go bedring Paul.")