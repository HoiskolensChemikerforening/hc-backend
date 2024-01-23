from django.shortcuts import render
from .forms import RefoundForm,RefoundFormSet
from .models import Refound

def index(request):
    form = RefoundForm()
    user = request.user
    formset = RefoundFormSet(queryset=Refound.objects.none())

    context = {
        "formset":formset,
        #"form":form,
        "user":user
    }
    return render(request ,"index.html", context)

def manage(request):
    pass





