from django.shortcuts import render_to_response
from .models import Committee


def index(request):
    # Fetch all members, who belong to a committee (Member -> Committee)
    # Group all these members by the committee type
    committees = Committee.objects.prefetch_related('member_set')

    context = {
        'committees': committees,
    }

    return render_to_response('committees/detail.html', context)
