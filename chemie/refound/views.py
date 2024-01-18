from django.shortcuts import render
from .forms import RefoundForm


def index(request):
    form = RefoundForm()

    context = {
        "form":form
    }
    return render(request ,"index.html", context)

def manage(request):
    pass





