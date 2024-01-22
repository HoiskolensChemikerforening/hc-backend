from django.shortcuts import render
from .forms import RefoundForm


def index(request):
    form = RefoundForm()
    user = request.user

    context = {
        "form":form,
        "user":user
    }
    return render(request ,"index.html", context)

def manage(request):
    pass





