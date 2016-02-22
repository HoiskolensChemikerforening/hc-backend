from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Submission

def get_name(request):
    if request.method == 'POST':
        form = Submission(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('thanks/')
    else:
        form = Submission()

    return render(request, 'shitbox/detail.html', {'form': form})

def thank_you(request):
    return render(request, 'shitbox/thank-you.html', {})
