from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Submission
from .forms import SubmissionForm

def submission_create(request):
    form = SubmissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
    context = {
        "form": form,
    }
    return render(request, "detail.html", context)

def get_name(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('thanks/')
    else:
        form = SubmissionForm()

    return render(request, 'shitbox/detail.html', {'form': form})

def thank_you(request):
    return render(request, 'shitbox/thank-you.html', {})
