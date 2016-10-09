from django.shortcuts import render
from .models import Committee
from .forms import EditCommittees


def index(request):
    # Fetch all members, who belong to a committee (Member -> Committee)
    # Group all these members by the committee type
    committees = Committee.objects.prefetch_related('member_set')

    context = {
        'committees': committees,
    }

    return render(request, 'committees/detail.html', context)

def edit(request):
    form = EditCommittees(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass
    context = {
        'form': form,
    }
    return render(request, 'committees/edit.html', context)